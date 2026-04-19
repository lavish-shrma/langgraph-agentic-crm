import asyncio
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.config import settings

async def test_models():
    models = [
        "llama-3.1-8b-instant",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ]
    for m in models:
        try:
            llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=m, max_retries=0)
            print(f"Testing {m}...")
            resp = await llm.ainvoke([HumanMessage(content="test")])
            print(f"SUCCESS {m}")
            pass
        except Exception as e:
            print(f"FAILED {m}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_models())
