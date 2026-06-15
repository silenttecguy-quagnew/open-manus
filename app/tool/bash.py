import asyncio
import os
import sys
from typing import Optional

from app.exceptions import ToolError
from app.tool.base import BaseTool, CLIResult


_BASH_DESCRIPTION = """Execute a command in the terminal."""


class _BashSession:
    """A session of a shell."""

    _started: bool
    _process: asyncio.subprocess.Process

    command: str = "powershell.exe" if sys.platform == "win32" else "bash"
    _output_delay: float = 0.2
    _timeout: float = 120.0
    _sentinel: str = "<<exit>>"

    def __init__(self):
        self._started = False
        self._timed_out = False

    async def start(self):
        if self._started:
            return

        self._process = await asyncio.create_subprocess_shell(
            self.command,
            shell=True,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        self._started = True

    def stop(self):
        """Terminate the shell."""
        if not self._started:
            raise ToolError("Session has not started.")
        if self._process.returncode is not None:
            return
        self._process.terminate()

    async def run(self, command: str):
        """Execute a command in the shell."""
        if not self._started:
            raise ToolError("Session has not started.")
        if self._process.returncode is not None:
            return CLIResult(
                system="tool must be restarted",
                error=f"shell has exited with returncode {self._process.returncode}",
            )
        
        assert self._process.stdin
        assert self._process.stdout
        assert self._process.stderr

        # send command
        self._process.stdin.write(
            command.encode() + f"; echo \"{self._sentinel}\"\n".encode()
        )
        await self._process.stdin.drain()

        output = ""
        error = ""
        try:
            async with asyncio.timeout(self._timeout):
                while True:
                    await asyncio.sleep(self._output_delay)
                    line = await self._process.stdout.readline()
                    line_text = line.decode()
                    if self._sentinel in line_text:
                        break
                    output += line_text
        except asyncio.TimeoutError:
            self._timed_out = True
            raise ToolError(f"timed out after {self._timeout} seconds")

        return CLIResult(output=output.strip(), error=error.strip())


class Bash(BaseTool):
    """A tool for executing shell commands"""

    name: str = "bash"
    description: str = _BASH_DESCRIPTION
    parameters: dict = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to execute.",
            },
        },
        "required": ["command"],
    }

    _session: Optional[_BashSession] = None

    async def execute(
        self, command: str | None = None, restart: bool = False, **kwargs
    ) -> CLIResult:
        if restart:
            if self._session:
                self._session.stop()
            self._session = _BashSession()
            await self._session.start()
            return CLIResult(system="tool has been restarted.")

        if self._session is None:
            self._session = _BashSession()
            await self._session.start()

        if command is not None:
            return await self._session.run(command)

        raise ToolError("no command provided.")
