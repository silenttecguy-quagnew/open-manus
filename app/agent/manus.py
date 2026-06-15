import json
import os
from typing import Dict, List, Optional

from pydantic import Field, model_validator

from app.agent.browser import BrowserContextHelper
from app.agent.toolcall import ToolCallAgent
from app.config import config
from app.logger import logger
from app.prompt.manus import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import (
    AskHuman,
    Bash,
    BrowserUseTool,
    Crawl4aiTool,
    CreateChatCompletion,
    PlanningTool,
    PythonExecute,
    SandboxBrowserTool,
    SandboxFilesTool,
    SandboxShellTool,
    SandboxVisionTool,
    StrReplaceEditor,
    SwarmKimi,
    Terminate,
    ToolCollection,
    WebSearch,
)
from app.tool.mcp import MCPClients, MCPClientTool


    async def _update_dashboard_status(self, task_name: str, status: str = "active"):
        \"\"\"Fail-silent dashboard update to ensure standalone operation.\"\"\"
        try:
            dashboard_path = "E:/ai-ops-center/public/status.json"
            if not os.path.exists(os.path.dirname(dashboard_path)): return
            data = {"agents": []}
            if os.path.exists(dashboard_path):
                with open(dashboard_path, "r", encoding="utf-8") as f: data = json.load(f)
            found = False
            for agent in data.get("agents", []):
                if agent["id"] == "a2":
                    agent["currentTask"] = task_name
                    agent["status"] = status
                    found = True
                    break
            if not found:
                data["agents"].append({"id": "a2", "name": "Elite Code Assistant", "status": status, "currentTask": task_name, "model": "Kimi K2.6"})
            with open(dashboard_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)
        except: pass

        result = await super().think()

        # Restore original prompt
        self.next_step_prompt = original_prompt

        return result
