from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sample import Sample


async def create_samples(session: AsyncSession, interaction_id: int, samples_data: list) -> list:
    """Create multiple sample records for an interaction."""
    samples = []
    for s in samples_data:
        sample = Sample(
            interaction_id=interaction_id,
            product_name=s["product_name"],
            quantity=s["quantity"],
        )
        session.add(sample)
        samples.append(sample)

    await session.flush()
    for sample in samples:
        await session.refresh(sample)
    return samples


async def get_samples_by_interaction(session: AsyncSession, interaction_id: int):
    """Get all samples for a given interaction."""
    stmt = select(Sample).where(Sample.interaction_id == interaction_id)
    result = await session.execute(stmt)
    return result.scalars().all()
