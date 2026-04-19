import asyncio
import sys
import os
from sqlalchemy import text

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import async_session_factory

async def check_followups():
    async with async_session_factory() as session:
        result = await session.execute(text('SELECT id, hcp_id, notes, follow_up_date, status FROM follow_up ORDER BY id DESC LIMIT 5'))
        rows = result.all()
        for row in rows:
            print(f"ID: {row[0]}, HCP_ID: {row[1]}, Notes: {row[2]}, Date: {row[3]}, Status: {row[4]}")

if __name__ == "__main__":
    asyncio.run(check_followups())
