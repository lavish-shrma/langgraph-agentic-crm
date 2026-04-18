import asyncio
from app.services.llm import get_secondary_llm
from langchain_core.messages import HumanMessage

async def test_llm():
    try:
        llm = get_secondary_llm()
        resp = await llm.ainvoke([HumanMessage(content="Hello, say test")])
        print("LLM RESPONSE:", resp.content)
    except Exception as e:
        print("LLM ERROR:", str(e))

if __name__ == "__main__":
    asyncio.run(test_llm())
