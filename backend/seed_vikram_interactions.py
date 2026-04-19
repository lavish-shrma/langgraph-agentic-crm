import asyncio
from datetime import date
from app.database import async_session_factory
from app.models.interaction import Interaction

async def seed_interactions():
    async with async_session_factory() as session:
        interactions = [
            Interaction(
                hcp_id=4,
                date=date(2026, 3, 15),
                interaction_type="Meeting",
                topics_discussed="GlucoStable efficacy and dosage optimization",
                sentiment="positive",
                outcome="Doctor agreed to prescribe GlucoStable to 3 diabetic patients",
                source="chat"
            ),
            Interaction(
                hcp_id=4,
                date=date(2026, 3, 28),
                interaction_type="Meeting",
                topics_discussed="NeuroCalm prescription trends and side effect profile",
                sentiment="neutral",
                outcome="Doctor requested more clinical trial data before prescribing",
                source="chat"
            ),
            Interaction(
                hcp_id=4,
                date=date(2026, 4, 10),
                interaction_type="Meeting",
                topics_discussed="GlucoStable patient follow-up results and CardioMax introduction",
                sentiment="positive",
                outcome="Positive feedback on GlucoStable, open to trialling CardioMax",
                source="chat"
            )
        ]
        session.add_all(interactions)
        await session.commit()
        print("3 interactions seeded for Dr. Vikram Patel (ID: 4)")

if __name__ == "__main__":
    asyncio.run(seed_interactions())
