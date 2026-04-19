import asyncio
from app.database import async_session_factory
from sqlalchemy import text

async def check():
    async with async_session_factory() as session:
        result = await session.execute(text("SELECT id, name, specialty FROM hcp ORDER BY id"))
        rows = result.fetchall()
        for r in rows:
            print(f"ID: {r[0]}, Name: {r[1]}, Specialty: {r[2]}")

if __name__ == "__main__":
    asyncio.run(check())
