import asyncio
import urllib.request
import json
import time

async def test():
    tests = [
        "Show me the full profile for Dr. Priya Sharma.",
        "Today I met Dr. Rajesh Mehta, discussed efficacy of CardioMax. Gave him 3 CardioMax 10mg samples. He was very positive and agreed to trial it. Follow up next week.",
        "Schedule a follow-up with Dr. Ananya Iyer on 2026-05-20 to discuss latest neurology clinical data.",
        "Summarize my last 3 visits with Dr. Vikram Patel.",
    ]
    
    for msg in tests:
        url = 'http://localhost:8000/api/agent/chat'
        data = json.dumps({'message': msg, 'conversation_history': []}).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        print(f"Testing: {msg[:50]}...")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read())
                print(f"MSG: {msg[:50]}")
                print(f"TOOLS: {resp.get('tools_used')}")
                print(f"RESPONSE: {resp.get('response')[:200]}")
                print("---")
        except Exception as e:
            print(f"ERROR for {msg[:20]}: {e}")
        
        # Large delay to avoid RPM limits
        print("Waiting 30s for next test...")
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(test())
