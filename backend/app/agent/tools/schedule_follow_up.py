import json
import logging
from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy import select

from app.database import async_session_factory
from app.models.follow_up import FollowUp
from app.models.interaction import Interaction

logger = logging.getLogger(__name__)


@tool
async def schedule_follow_up(interaction_id: int, follow_up_date: str, notes: str = "") -> str:
    """Schedule a follow-up for an HCP interaction.

    Args:
        interaction_id: The ID of the interaction to schedule a follow-up for.
        follow_up_date: The follow-up date in YYYY-MM-DD format.
        notes: Optional notes for the follow-up.
    """
    try:
        parsed_date = datetime.strptime(follow_up_date, "%Y-%m-%d").date()

        async with async_session_factory() as session:
            # Get the interaction to find hcp_id
            stmt = select(Interaction).where(Interaction.id == interaction_id)
            result = await session.execute(stmt)
            interaction = result.scalar_one_or_none()

            if not interaction:
                return json.dumps({
                    "success": False,
                    "message": f"Interaction with ID {interaction_id} not found.",
                })

            # Create FollowUp record
            follow_up = FollowUp(
                interaction_id=interaction_id,
                hcp_id=interaction.hcp_id,
                follow_up_date=parsed_date,
                notes=notes or None,
                status="pending",
            )
            session.add(follow_up)

            # Update follow_up_date on the interaction
            interaction.follow_up_date = parsed_date
            await session.commit()

            return json.dumps({
                "success": True,
                "follow_up_id": follow_up.id,
                "message": f"Follow-up scheduled for {follow_up_date}. Notes: {notes or 'None'}",
                "follow_up_date": follow_up_date,
            })

    except ValueError:
        return json.dumps({
            "success": False,
            "message": "Invalid date format. Please use YYYY-MM-DD format.",
        })
    except Exception as e:
        logger.error(f"Error in schedule_follow_up tool: {e}")
        return json.dumps({
            "success": False,
            "message": f"Error scheduling follow-up: {str(e)}",
        })
