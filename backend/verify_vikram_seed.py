import asyncio
from app.database import async_session_factory
from sqlalchemy import text

async def check():
    async with async_session_factory() as session:
        result = await session.execute(text("SELECT id, hcp_id, topics_discussed, sentiment, date FROM interaction WHERE hcp_id = 4 ORDER BY date"))
        rows = result.fetchall()
        for r in rows:
            print(f"ID: {r[0]}, HCP_ID: {r[1]}, Topics: {r[2]}, Sentiment: {r[3]}, Date: {r[4]}")

if __name__ == "__main__":
    asyncio.run(check())
