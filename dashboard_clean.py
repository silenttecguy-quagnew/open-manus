import io;
f=io.open('app/agent/manus.py', 'r', encoding='utf-8');
content=f.read();
f.close();
# Force clean the messy injection
bad_block = 'try:\n            last_msg = self.memory.messages[-1].content if self.memory.messages else \"Starting task\"\n            import asyncio; asyncio.create_task(self._update_dashboard_status(str(last_msg)[:50] + \"...\"))\n        except: pass\n        '
content = content.replace(bad_block, '')
marker = 'result = await super().think()'
clean_injection = '        try:\n            last_msg = self.memory.messages[-1].content if self.memory.messages else \"Starting task\"\n            import asyncio; asyncio.create_task(self._update_dashboard_status(str(last_msg)[:50] + \"...\"))\n        except: pass\n\n        '
content = content.replace(marker, clean_injection + marker)
f=io.open('app/agent/manus.py', 'w', encoding='utf-8');
f.write(content);
f.close()
