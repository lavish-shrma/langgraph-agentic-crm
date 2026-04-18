from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.interaction import Interaction
from app.models.sample import Sample


async def create_interaction(session: AsyncSession, data: dict) -> Interaction:
    """Create a new interaction with optional samples."""
    samples_data = data.pop("samples", None) or []

    interaction = Interaction(**data)
    session.add(interaction)
    await session.flush()

    for s in samples_data:
        sample = Sample(
            interaction_id=interaction.id,
            product_name=s["product_name"],
            quantity=s["quantity"],
        )
        session.add(sample)

    await session.flush()
    await session.refresh(interaction)
    return interaction


async def get_interactions(
    session: AsyncSession,
    hcp_id: int = None,
    limit: int = 10,
    offset: int = 0,
):
    """Get paginated list of interactions, optionally filtered by HCP."""
    stmt = select(Interaction).options(selectinload(Interaction.samples))
    if hcp_id:
        stmt = stmt.where(Interaction.hcp_id == hcp_id)
    stmt = stmt.order_by(Interaction.date.desc(), Interaction.created_at.desc())
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_interaction_by_id(session: AsyncSession, interaction_id: int):
    """Get a single interaction by ID with samples."""
    stmt = (
        select(Interaction)
        .options(selectinload(Interaction.samples))
        .where(Interaction.id == interaction_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_interaction(session: AsyncSession, interaction_id: int, data: dict) -> Interaction:
    """Partial update an interaction."""
    stmt = select(Interaction).where(Interaction.id == interaction_id)
    result = await session.execute(stmt)
    interaction = result.scalar_one_or_none()

    if not interaction:
        return None

    for key, value in data.items():
        if hasattr(interaction, key) and value is not None:
            setattr(interaction, key, value)

    await session.flush()
    await session.refresh(interaction)
    return interaction
