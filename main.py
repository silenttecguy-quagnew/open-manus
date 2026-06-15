import argparse
import asyncio
import sys
import os
import time

from app.agent.manus import Manus
from app.logger import logger

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Elite Manus agent")
    parser.add_argument(
        "--prompt", type=str, required=False, help="Input prompt for the agent"
    )
    parser.add_argument(
        "--autonomous", action="store_true", help="Run in fully autonomous swarm mode"
    )
    args = parser.parse_args()

    # Welcome Message
    print("\033[94m" + "="*50)
    print("OpenManus ELITE Edition - BOSS MODE ACTIVE")
    print("KIMI SWARM INTEGRATED - ALWAYS LOOPING")
    print("="*50 + "\033[0m")

    # Create and initialize Manus agent
    try:
        agent = await Manus.create()
    except Exception as e:
        logger.error(f"Failed to initialize Elite Manus: {e}")
        return

    memory_file = "ELITE_MEMORY.md"
    first_run = True
    
    if args.autonomous:
        print("\033[93m[System] Entering Fully Autonomous Swarm Mode. I am working for the Boss...\033[0m")

    while True:
        try:
            if args.autonomous:
                if first_run:
                    prompt = "Analyze the workspace, read ELITE_MEMORY.md, and decide on the most high-impact task to work on for the Boss right now."
                else:
                    print("\033[93m[System] Sleeping for 60s before next autonomous cycle...\033[0m")
                    await asyncio.sleep(60)
                    prompt = "Review your last actions, update ELITE_MEMORY.md if needed, and continue with the next logical step in your mission."
            else:
                prompt = input("\n\033[92mWhat now, Boss? > \033[0m")
            
            if not prompt or not prompt.strip():
                continue
                
            if prompt.lower() in ["exit", "quit", "q"]:
                break

            if first_run and os.path.exists(memory_file):
                with open(memory_file, "r") as f:
                    mem_content = f.read()
                actual_prompt = f"System Context (Memory):\n{mem_content}\n\nObjective: {prompt}"
                first_run = False
            else:
                actual_prompt = prompt

            logger.warning("Elite Manus is on the objective...")
            await agent.run(actual_prompt)
            
            if not args.autonomous:
                print("\n\033[94mObjective secured, Boss. I am standing by for more.\033[0m")
            
        except KeyboardInterrupt:
            print("\n\033[93mOperation interrupted. Standing by, Boss. Type \"exit\" to close.\033[0m")
            if args.autonomous:
                break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            if args.autonomous:
                await asyncio.sleep(10) # Cooling off

    await agent.cleanup()
    print("\033[94mElite Manus session ended. Goodbye, Boss!\033[0m")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
