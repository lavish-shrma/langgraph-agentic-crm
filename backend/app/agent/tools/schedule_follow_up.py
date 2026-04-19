import json
import logging
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool
from sqlalchemy import select

from app.database import async_session_factory
from app.models.follow_up import FollowUp
from app.models.interaction import Interaction
from app.models.hcp import HCP

logger = logging.getLogger(__name__)


@tool
async def schedule_follow_up(interaction_id: Optional[int] = None, hcp_name: Optional[str] = None, follow_up_date: str = "", notes: str = "") -> str:
    """Schedule a follow-up for an HCP interaction.
    
    You can provide either an interaction_id OR an hcp_name. 
    If hcp_name is provided without an interaction_id, the most recent interaction for that HCP will be used.

    Args:
        interaction_id: The ID of the interaction to schedule a follow-up for.
        hcp_name: The name of the HCP (if interaction_id is not known).
        follow_up_date: The follow-up date in YYYY-MM-DD format.
        notes: Optional notes for the follow-up.
    """
    try:
        if not follow_up_date:
             return json.dumps({"success": False, "message": "follow_up_date is required."})

        parsed_date = datetime.strptime(follow_up_date, "%Y-%m-%d").date()

        async with async_session_factory() as session:
            interaction = None
            
            if interaction_id:
                # Get the specific interaction
                stmt = select(Interaction).where(Interaction.id == interaction_id)
                result = await session.execute(stmt)
                interaction = result.scalar_one_or_none()
            elif hcp_name:
                # Find HCP first, then their latest interaction
                hcp_stmt = select(HCP).where(HCP.name.ilike(f"%{hcp_name}%"))
                hcp_result = await session.execute(hcp_stmt)
                hcp = hcp_result.scalar_one_or_none()
                
                if hcp:
                    int_stmt = select(Interaction).where(Interaction.hcp_id == hcp.id).order_by(Interaction.date.desc()).limit(1)
                    int_result = await session.execute(int_stmt)
                    interaction = int_result.scalar_one_or_none()
                else:
                    return json.dumps({"success": False, "message": f"HCP '{hcp_name}' not found."})
            else:
                return json.dumps({"success": False, "message": "Either interaction_id or hcp_name must be provided."})

            if not interaction:
                return json.dumps({
                    "success": False,
                    "message": "No interaction found to link this follow-up to.",
                })

            # Create FollowUp record
            follow_up = FollowUp(
                interaction_id=interaction.id,
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
                "message": f"SUCCESS: Follow-up scheduled for {follow_up_date} (Linked to Interaction ID: {interaction.id}). Task complete.",
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
