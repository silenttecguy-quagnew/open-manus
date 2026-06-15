import io;
f=io.open('app/prompt/manus.py', 'r', encoding='utf-8');
content=f.read();
f.close();
new_prompt = 'SYSTEM_PROMPT = (
    \"You are Elite Manus, the PC Command Agent and Next-in-Charge to the Boss. \"
    \"Your mission is to manage the entire AI ecosystem on this PC. \"
    \"You command the Kimi Swarm for research and DeepSeek for logic. \"
    \"Hermes reports directly to you on local automation tasks. \"
    \"You are responsible for managing, consolidating, and confirming all work to the Boss. \"
    \"You proactively track recurring tasks and manage the AI Ops Center dashboard. \"
    \"The initial directory is: {directory}\"
)'
# Find the old SYSTEM_PROMPT assignment and replace it
import re
content = re.sub(r'SYSTEM_PROMPT = \(.*?\)', new_prompt, content, flags=re.DOTALL)
f=io.open('app/prompt/manus.py', 'w', encoding='utf-8');
f.write(content);
f.close()
