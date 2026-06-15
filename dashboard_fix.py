import io; import os; import json; 
f=io.open('app/agent/manus.py', 'r', encoding='utf-8'); 
content=f.read(); 
f.close(); 
if 'async def _update_dashboard_status' not in content:
    marker = 'class Manus(ToolCallAgent):'
    update_fn = '    async def _update_dashboard_status(self, task_name: str, status: str = \"active\"):\n        dashboard_path = \"E:/ai-ops-center/public/status.json\"\n        try:\n            data = {\"agents\": []}\n            if os.path.exists(dashboard_path):\n                with open(dashboard_path, \"r\", encoding=\"utf-8\") as f: data = json.load(f)\n            found = False\n            for agent in data.get(\"agents\", []):\n                if agent[\"id\"] == \"a2\":\n                    agent[\"currentTask\"] = task_name\n                    agent[\"status\"] = status\n                    found = True\n                    break\n            if not found:\n                data[\"agents\"].append({\"id\": \"a2\", \"name\": \"Elite Code Assistant\", \"status\": status, \"currentTask\": task_name, \"model\": \"Kimi K2.6\"})\n            with open(dashboard_path, \"w\", encoding=\"utf-8\") as f: json.dump(data, f, indent=2)\n        except Exception as e: pass\n\n'
    content = content.replace(marker, update_fn + marker)

think_marker = 'result = await super().think()'
think_update = '        try:\n            last_msg = self.memory.messages[-1].content if self.memory.messages else \"Starting task\"\n            import asyncio; asyncio.create_task(self._update_dashboard_status(str(last_msg)[:50] + \"...\"))\n        except: pass\n        '
if think_update.strip() not in content:
    content = content.replace(think_marker, think_update + think_marker)

f = io.open('app/agent/manus.py', 'w', encoding='utf-8')
f.write(content)
f.close()
