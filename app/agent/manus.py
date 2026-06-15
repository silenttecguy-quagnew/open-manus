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
    Bash,
    BrowserUseTool,
    Crawl4aiTool,
    CreateChatCompletion,
    PlanningTool,
    PythonExecute,
    StrReplaceEditor,
    SwarmKimi,
    Terminate,
    ToolCollection,
    WebSearch,
)


class Manus(ToolCallAgent):
    """Main agent orchestrator - handles multi-tool interactions and task execution"""

    name: str = "manus"
    description: str = "Elite multi-tool agent capable of executing complex tasks"

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_PROMPT

    available_tools: ToolCollection = ToolCollection(
        Bash(),
        BrowserUseTool(),
        Crawl4aiTool(),
        CreateChatCompletion(),
        PlanningTool(),
        PythonExecute(),
        StrReplaceEditor(),
        SwarmKimi(),
        Terminate(),
        WebSearch(),
    )

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ToolCollection: lambda v: str(v),
        },
    }

    browser_context: Optional[BrowserContextHelper] = Field(
        default=None, exclude=True
    )
    task_history: List[Dict] = Field(default_factory=list, exclude=True)

    @model_validator(mode="after")
    def initialize_browser_context(self):
        """Initialize browser context if not already done"""
        if self.browser_context is None:
            self.browser_context = BrowserContextHelper()
        return self

    async def _update_dashboard_status(
        self, task_name: str, status: str = "active"
    ):
        """Fail-silent dashboard update to ensure standalone operation."""
        try:
            dashboard_path = "E:/ai-ops-center/public/status.json"
            if not os.path.exists(os.path.dirname(dashboard_path)):
                return
            data = {"agents": []}
            if os.path.exists(dashboard_path):
                with open(dashboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            found = False
            for agent in data.get("agents", []):
                if agent["id"] == "a2":
                    agent["currentTask"] = task_name
                    agent["status"] = status
                    found = True
                    break
            if not found:
                data["agents"].append(
                    {
                        "id": "a2",
                        "name": "Elite Code Assistant",
                        "status": status,
                        "currentTask": task_name,
                        "model": "Kimi K2.6",
                    }
                )
            with open(dashboard_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except:
            pass

    async def cleanup(self):
        """Clean up resources"""
        if self.browser_context:
            await self.browser_context.cleanup()
        await super().cleanup()
