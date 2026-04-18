import asyncio
from app.agent.graph import agent_graph
from langchain_core.messages import HumanMessage, SystemMessage
from app.agent.prompts import SYSTEM_PROMPT

async def test_summarize():
    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content="Summarize my last visits with Dr. Priya Sharma")
        ]
    }
    
    try:
        print("Invoking agent graph...")
        result = await agent_graph.ainvoke(initial_state)
        print("Final response:")
        for msg in result["messages"]:
            print(f"[{msg.type}]: {msg.content}")
            if hasattr(msg, "tool_calls"):
                print("  Tool calls:", msg.tool_calls)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_summarize())
