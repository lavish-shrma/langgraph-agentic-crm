import asyncio
from app.agent.graph import agent_graph
from langchain_core.messages import HumanMessage, SystemMessage
from app.agent.prompts import SYSTEM_PROMPT
import logging

logging.basicConfig(level=logging.INFO)

async def test_stream():
    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content="Summarize my last visits with Dr. Priya Sharma")
        ]
    }
    
    print("Starting agent stream...", flush=True)
    try:
        async for s in agent_graph.astream(initial_state):
            print("Step Output:", s, flush=True)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_stream())
