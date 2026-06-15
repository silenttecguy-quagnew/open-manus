import io, os, json, re;
f=io.open("app/agent/manus.py", "r", encoding="utf-8");
c=f.read();
f.close();
new_fn = """    async def _update_dashboard_status(self, task_name: str, status: str = "active"):
        \\"\\"\\"Fail-silent dashboard update to ensure standalone operation.\\"\\"\\"
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
        except: pass"""
c = re.sub(r"    async def _update_dashboard_status.*?except: pass", new_fn, c, flags=re.DOTALL)
f=io.open("app/agent/manus.py", "w", encoding="utf-8");
f.write(c);
f.close()
