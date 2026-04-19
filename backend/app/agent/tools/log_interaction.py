import json
import logging
from datetime import date, datetime
from typing import Optional

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from app.database import async_session_factory
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.sample import Sample
from app.services.llm import get_primary_llm, invoke_with_retry
from sqlalchemy import select

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are a data extraction assistant. Extract structured fields from the following natural language description of an HCP (Healthcare Professional) interaction.

Return ONLY a valid JSON object with these fields (use null for missing fields):
{{
  "hcp_name": "string - full name of the doctor/HCP",
  "interaction_type": "string - one of: Meeting, Call, Email, Conference Visit, Other",
  "date": "string - YYYY-MM-DD format, use today's date if not specified",
  "time": "string - HH:MM format or null",
  "attendees": "string - comma-separated list of attendees or null",
  "topics_discussed": "string - main topics discussed",
  "materials_shared": ["array of strings - materials/documents shared"],
  "samples": [
    {{"product_name": "string", "quantity": number}}
  ],
  "sentiment": "string - one of: positive, neutral, negative",
  "outcome": "string - outcome or result of the interaction",
  "follow_up_notes": "string - any follow-up notes or null",
  "follow_up_date": "string - YYYY-MM-DD format or null"
}}

Today's date is {today}.

IMPORTANT: Return ONLY the JSON object. No markdown fences, no preamble, no explanation. Just the JSON.

Natural language description:
{text}"""


@tool
async def log_interaction(text: str, hcp_name: Optional[str] = None, interaction_type: Optional[str] = None, date_str: Optional[str] = None) -> str:
    """Log a new HCP interaction from natural language text or structured data.

    Args:
        text: Natural language description of the interaction OR structured summary.
        hcp_name: Optional explicit HCP name (if already known).
        interaction_type: Optional explicit interaction type.
        date_str: Optional explicit date in YYYY-MM-DD format.
    """
    try:
        # Use LLM to extract structured data from natural language
        llm = get_primary_llm()
        today = date.today().isoformat()

        extraction_messages = [
            HumanMessage(content=EXTRACTION_PROMPT.format(today=today, text=text))
        ]

        response = await invoke_with_retry(llm, extraction_messages)
        response_text = response.content.strip()

        # Clean up response - remove markdown fences if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
            response_text = response_text.strip()

        if response_text.startswith("{") is False:
            # Try to find JSON in the response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                response_text = response_text[start:end]

        extracted = json.loads(response_text)
        logger.info(f"Extracted fields: {extracted}")

        # Override with explicit values if provided
        if hcp_name:
            extracted["hcp_name"] = hcp_name
        if interaction_type:
            extracted["interaction_type"] = interaction_type
        if date_str:
            extracted["date"] = date_str

        # Validate required fields
        if not extracted.get("hcp_name"):
            return json.dumps({
                "success": False,
                "message": "Could not extract the HCP name. Please specify the doctor's name.",
            })

        if not extracted.get("interaction_type"):
            extracted["interaction_type"] = "Meeting"

        if not extracted.get("date"):
            extracted["date"] = today

        # Look up HCP in database
        async with async_session_factory() as session:
            stmt = select(HCP).where(HCP.name.ilike(f"%{extracted['hcp_name']}%"))
            result = await session.execute(stmt)
            hcp = result.scalar_one_or_none()

            if not hcp:
                return json.dumps({
                    "success": False,
                    "message": f"Could not find HCP '{extracted['hcp_name']}' in the database. Please check the name and try again.",
                })

            # Parse date and time
            interaction_date = extracted["date"]
            if isinstance(interaction_date, str):
                interaction_date = datetime.strptime(interaction_date, "%Y-%m-%d").date()

            interaction_time = None
            if extracted.get("time"):
                try:
                    interaction_time = datetime.strptime(extracted["time"], "%H:%M").time()
                except (ValueError, TypeError):
                    pass

            # Parse follow_up_date
            follow_up_date = None
            if extracted.get("follow_up_date"):
                try:
                    follow_up_date = datetime.strptime(extracted["follow_up_date"], "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    pass

            # Create Interaction record
            interaction = Interaction(
                hcp_id=hcp.id,
                interaction_type=extracted.get("interaction_type", "Meeting"),
                date=interaction_date,
                time=interaction_time,
                attendees=extracted.get("attendees"),
                topics_discussed=extracted.get("topics_discussed"),
                materials_shared=extracted.get("materials_shared") or [],
                sentiment=extracted.get("sentiment"),
                outcome=extracted.get("outcome"),
                follow_up_notes=extracted.get("follow_up_notes"),
                follow_up_date=follow_up_date,
                location=hcp.institution,
                source="chat",
            )
            session.add(interaction)
            await session.flush()

            # Create Sample records
            samples_data = extracted.get("samples") or []
            for s in samples_data:
                if s and s.get("product_name") and s.get("quantity"):
                    sample = Sample(
                        interaction_id=interaction.id,
                        product_name=s["product_name"],
                        quantity=int(s["quantity"]),
                    )
                    session.add(sample)

            await session.commit()

            # Generate follow-up suggestions
            follow_ups = [
                f"Follow up with {hcp.name} to discuss {extracted.get('topics_discussed', 'previous topics')} progress",
                f"Share additional clinical data on {extracted.get('materials_shared', ['discussed products'])[0] if extracted.get('materials_shared') else 'discussed products'} with {hcp.name}",
                f"Schedule next visit with {hcp.name} at {hcp.institution} to review patient outcomes",
            ]

            return json.dumps({
                "success": True,
                "interaction_id": interaction.id,
                "message": f"Interaction logged successfully. ID: {interaction.id}",
                "suggested_follow_ups": follow_ups,
                "extracted_fields": {
                    "hcp_id": hcp.id,
                    "hcp_name": hcp.name,
                    "interaction_type": extracted.get("interaction_type"),
                    "date": str(extracted.get("date")) if extracted.get("date") else None,
                    "time": extracted.get("time"),
                    "attendees": extracted.get("attendees"),
                    "topics_discussed": extracted.get("topics_discussed"),
                    "materials_shared": extracted.get("materials_shared", []),
                    "sentiment": extracted.get("sentiment"),
                    "outcome": extracted.get("outcome"),
                    "follow_up_notes": extracted.get("follow_up_notes"),
                    "follow_up_date": str(extracted.get("follow_up_date")) if extracted.get("follow_up_date") else None,
                    "location": hcp.institution,
                    "samples_distributed": extracted.get("samples") or [],
                },
            })

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return json.dumps({
            "success": False,
            "message": "Failed to extract structured data from the description. Please try rephrasing.",
        })
    except Exception as e:
        logger.error(f"Error in log_interaction tool: {e}")
        return json.dumps({
            "success": False,
            "message": f"Error logging interaction: {str(e)}",
        })
