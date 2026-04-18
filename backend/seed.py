"""Seed script to populate the database with initial HCP and interaction data."""

import asyncio
import sys
import os
from datetime import date, time, timedelta
import random

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import async_session_factory, engine, Base
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.sample import Sample


HCPS = [
    {
        "name": "Dr. Priya Sharma",
        "specialty": "Cardiology",
        "institution": "Apollo Hospital, Mumbai",
        "email": "priya.sharma@apollo.com",
        "phone": "+91-9876543210",
        "location": "Mumbai, Maharashtra",
    },
    {
        "name": "Dr. Rajesh Mehta",
        "specialty": "Oncology",
        "institution": "Tata Memorial Hospital, Mumbai",
        "email": "rajesh.mehta@tatamemorial.com",
        "phone": "+91-9876543211",
        "location": "Mumbai, Maharashtra",
    },
    {
        "name": "Dr. Ananya Iyer",
        "specialty": "Neurology",
        "institution": "NIMHANS, Bangalore",
        "email": "ananya.iyer@nimhans.ac.in",
        "phone": "+91-9876543212",
        "location": "Bangalore, Karnataka",
    },
    {
        "name": "Dr. Vikram Patel",
        "specialty": "Endocrinology",
        "institution": "AIIMS, New Delhi",
        "email": "vikram.patel@aiims.edu",
        "phone": "+91-9876543213",
        "location": "New Delhi, Delhi",
    },
    {
        "name": "Dr. Sunita Reddy",
        "specialty": "Pulmonology",
        "institution": "KIMS Hospital, Hyderabad",
        "email": "sunita.reddy@kims.com",
        "phone": "+91-9876543214",
        "location": "Hyderabad, Telangana",
    },
    {
        "name": "Dr. Arjun Nair",
        "specialty": "Cardiology",
        "institution": "Fortis Hospital, Chennai",
        "email": "arjun.nair@fortis.com",
        "phone": "+91-9876543215",
        "location": "Chennai, Tamil Nadu",
    },
    {
        "name": "Dr. Meera Gupta",
        "specialty": "Oncology",
        "institution": "Max Hospital, New Delhi",
        "email": "meera.gupta@maxhospital.com",
        "phone": "+91-9876543216",
        "location": "New Delhi, Delhi",
    },
    {
        "name": "Dr. Sanjay Deshmukh",
        "specialty": "Neurology",
        "institution": "KEM Hospital, Pune",
        "email": "sanjay.deshmukh@kem.edu",
        "phone": "+91-9876543217",
        "location": "Pune, Maharashtra",
    },
]

INTERACTION_TEMPLATES = [
    {
        "interaction_type": "Meeting",
        "topics_discussed": "Discussed efficacy of CardioMax in managing hypertension. Reviewed latest clinical trial data showing 40% improvement in patient outcomes.",
        "materials_shared": ["CardioMax Efficacy Brochure", "Clinical Trial Results Q4"],
        "sentiment": "positive",
        "outcome": "Doctor agreed to trial CardioMax on 5 patients over the next month.",
        "follow_up_notes": "Follow up to check patient trial progress.",
        "samples": [{"product_name": "CardioMax 10mg", "quantity": 3}],
    },
    {
        "interaction_type": "Call",
        "topics_discussed": "Follow-up call regarding NeuroCalm prescription trends. Doctor reported positive patient feedback on reduced side effects.",
        "materials_shared": ["NeuroCalm Safety Profile"],
        "sentiment": "positive",
        "outcome": "Doctor will continue prescribing NeuroCalm for anxiety patients.",
        "follow_up_notes": "Send updated prescribing guidelines.",
        "samples": [],
    },
    {
        "interaction_type": "Meeting",
        "topics_discussed": "Presented new diabetes management solution GlucoStable. Compared pricing with competitor products. Doctor expressed concerns about cost for patients.",
        "materials_shared": ["GlucoStable Product Sheet", "Pricing Comparison Chart"],
        "sentiment": "neutral",
        "outcome": "Doctor requested more information on patient assistance programs.",
        "follow_up_notes": "Prepare patient assistance program details and schedule follow-up.",
        "samples": [{"product_name": "GlucoStable 500mg", "quantity": 5}],
    },
    {
        "interaction_type": "Conference Visit",
        "topics_discussed": "Met at National Pharma Conference. Discussed upcoming product launches and clinical pipeline. Doctor showed interest in oncology portfolio.",
        "materials_shared": ["Conference Presentation Slides", "Pipeline Overview"],
        "sentiment": "positive",
        "outcome": "Doctor interested in participating as KOL for upcoming product launch.",
        "follow_up_notes": "Send KOL program details and honorarium structure.",
        "samples": [],
    },
    {
        "interaction_type": "Email",
        "topics_discussed": "Shared latest research paper on RespiClear lung function benefits. Doctor acknowledged receipt and will review for potential prescription.",
        "materials_shared": ["RespiClear Research Paper PDF"],
        "sentiment": "neutral",
        "outcome": "Awaiting doctor's review and feedback on the research findings.",
        "follow_up_notes": "Call in 1 week to discuss research paper findings.",
        "samples": [],
    },
    {
        "interaction_type": "Meeting",
        "topics_discussed": "In-clinic presentation on OncoShield immunotherapy benefits. Showed survival rate data from Phase III trials.",
        "materials_shared": ["OncoShield Phase III Data", "Treatment Protocol Guide"],
        "sentiment": "positive",
        "outcome": "Doctor plans to recommend OncoShield for eligible cancer patients.",
        "follow_up_notes": "Arrange product training session for clinic staff.",
        "samples": [{"product_name": "OncoShield 100mg", "quantity": 2}],
    },
]


async def seed_database():
    """Populate the database with seed data."""
    async with async_session_factory() as session:
        # Check if data already exists
        from sqlalchemy import select, func
        count_result = await session.execute(select(func.count(HCP.id)))
        existing_count = count_result.scalar()

        if existing_count > 0:
            print(f"Database already has {existing_count} HCPs. Skipping seed.")
            return

        print("Seeding database...")

        # Create HCPs
        hcp_objects = []
        for hcp_data in HCPS:
            hcp = HCP(**hcp_data)
            session.add(hcp)
            hcp_objects.append(hcp)

        await session.flush()
        print(f"Created {len(hcp_objects)} HCPs.")

        # Create interactions (3 per HCP)
        interaction_count = 0
        sample_count = 0

        for hcp in hcp_objects:
            for i in range(3):
                template = INTERACTION_TEMPLATES[random.randint(0, len(INTERACTION_TEMPLATES) - 1)]
                days_ago = random.randint(1, 90)
                interaction_date = date.today() - timedelta(days=days_ago)
                interaction_time = time(hour=random.randint(9, 17), minute=random.choice([0, 15, 30, 45]))

                interaction = Interaction(
                    hcp_id=hcp.id,
                    interaction_type=template["interaction_type"],
                    date=interaction_date,
                    time=interaction_time,
                    attendees=f"Field Rep, {hcp.name}",
                    topics_discussed=template["topics_discussed"],
                    materials_shared=template["materials_shared"],
                    sentiment=template["sentiment"],
                    outcome=template["outcome"],
                    follow_up_notes=template["follow_up_notes"],
                    follow_up_date=interaction_date + timedelta(days=14),
                    location=hcp.institution,
                    source="form",
                )
                session.add(interaction)
                await session.flush()
                interaction_count += 1

                # Add samples
                for s in template.get("samples", []):
                    sample = Sample(
                        interaction_id=interaction.id,
                        product_name=s["product_name"],
                        quantity=s["quantity"],
                    )
                    session.add(sample)
                    sample_count += 1

        await session.commit()
        print(f"Created {interaction_count} interactions and {sample_count} samples.")
        print("Seed complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())
