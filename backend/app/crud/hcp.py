from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hcp import HCP


async def search_hcps(session: AsyncSession, query: str = ""):
    """Search HCPs by name (case-insensitive partial match)."""
    stmt = select(HCP)
    if query:
        stmt = stmt.where(HCP.name.ilike(f"%{query}%"))
    stmt = stmt.order_by(HCP.name)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_hcp_by_id(session: AsyncSession, hcp_id: int):
    """Get a single HCP by ID."""
    stmt = select(HCP).where(HCP.id == hcp_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_hcp_by_name(session: AsyncSession, name: str):
    """Get a single HCP by exact name (case-insensitive)."""
    stmt = select(HCP).where(HCP.name.ilike(name))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
