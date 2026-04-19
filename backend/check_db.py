import asyncio
import sys
import os
from sqlalchemy import select

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import async_session_factory
from app.models.hcp import HCP
from app.models.interaction import Interaction

async def check_db():
    async with async_session_factory() as session:
        # Check HCPs
        r = await session.execute(select(HCP.name))
        hcp_names = [x[0] for x in r.all()]
        print(f"HCP Names in DB: {hcp_names}")
        
        # Check for Ananya
        r = await session.execute(select(HCP).where(HCP.name.ilike('%Ananya%')))
        hcp = r.scalar_one_or_none()
        if hcp:
            print(f"Found HCP: {hcp.name} (ID: {hcp.id})")
            r = await session.execute(select(Interaction).where(Interaction.hcp_id == hcp.id))
            interactions = r.scalars().all()
            print(f"Interactions for {hcp.name}: {[i.id for i in interactions]}")
        else:
            print("Dr. Ananya Iyer NOT found in DB.")

if __name__ == "__main__":
    asyncio.run(check_db())
