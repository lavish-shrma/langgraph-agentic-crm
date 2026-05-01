import httpx
import asyncio
import json
import sys

async def run(message, out_file):
    async with httpx.AsyncClient(timeout=180.0) as client:
        r = await client.post("http://localhost:8000/api/agent/chat", json={"message": message, "conversation_history": []})
        data = r.json()
        with open(out_file, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    msg = sys.argv[1]
    out = sys.argv[2]
    asyncio.run(run(msg, out))
