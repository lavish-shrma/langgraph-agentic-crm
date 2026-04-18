from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.follow_up import FollowUp


async def create_follow_up(session: AsyncSession, data: dict) -> FollowUp:
    """Create a new follow-up."""
    follow_up = FollowUp(**data)
    session.add(follow_up)
    await session.flush()
    await session.refresh(follow_up)
    return follow_up


async def get_follow_ups(
    session: AsyncSession,
    hcp_id: int = None,
    status: str = None,
):
    """Get filtered list of follow-ups."""
    stmt = select(FollowUp)
    if hcp_id:
        stmt = stmt.where(FollowUp.hcp_id == hcp_id)
    if status:
        stmt = stmt.where(FollowUp.status == status)
    stmt = stmt.order_by(FollowUp.follow_up_date.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_follow_up(session: AsyncSession, follow_up_id: int, data: dict) -> FollowUp:
    """Update a follow-up."""
    stmt = select(FollowUp).where(FollowUp.id == follow_up_id)
    result = await session.execute(stmt)
    follow_up = result.scalar_one_or_none()

    if not follow_up:
        return None

    for key, value in data.items():
        if hasattr(follow_up, key) and value is not None:
            setattr(follow_up, key, value)

    await session.flush()
    await session.refresh(follow_up)
    return follow_up
