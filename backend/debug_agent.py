import asyncio
import sys
import os
import json
import logging
from datetime import date

# Configure logging to capture everything
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agent.graph import agent_graph
from app.agent.state import AgentState
from langchain_core.messages import HumanMessage

async def debug_agent(message: str):
    print(f"\n--- Testing message: {message} ---")
    state = {
        "messages": [HumanMessage(content=message)],
    }
    
    try:
        async for output in agent_graph.astream(state):
            for node, data in output.items():
                print(f"\n[Node: {node}]")
                if "messages" in data:
                    for msg in data["messages"]:
                        content = msg.content if hasattr(msg, 'content') else str(msg)
                        print(f"Message: {content}")
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            print(f"Tool Calls: {msg.tool_calls}")
    except Exception as e:
        print(f"\nERROR: {str(e)}")

if __name__ == "__main__":
    test_msg = "Schedule a follow-up with Dr. Ananya Iyer on 2026-05-20 to discuss latest neurology clinical data."
    asyncio.run(debug_agent(test_msg))
