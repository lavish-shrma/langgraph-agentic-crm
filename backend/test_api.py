import httpx
import asyncio
import json

async def run():
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post("http://localhost:8000/api/agent/chat", json={"message": "Summarize my last 3 visits with Dr. Vikram Patel.", "conversation_history": []})
        with open("test_api_out.json", "w") as f:
            json.dump(r.json(), f, indent=2)

asyncio.run(run())
