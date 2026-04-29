import asyncio
from app.database import async_session_factory
from sqlalchemy import text

async def check():
    async with async_session_factory() as session:
        result = await session.execute(text("SELECT id, hcp_id, topics_discussed FROM interaction WHERE hcp_id = 4 ORDER BY id"))
        rows = result.fetchall()
        for r in rows:
            print(f"ID: {r[0]}, HCP: {r[1]}, Topics: {r[2]}")

asyncio.run(check())
