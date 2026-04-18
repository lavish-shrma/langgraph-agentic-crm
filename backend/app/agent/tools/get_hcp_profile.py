import json
import logging
from typing import Optional

from langchain_core.tools import tool
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import async_session_factory
from app.models.hcp import HCP
from app.models.interaction import Interaction

logger = logging.getLogger(__name__)


@tool
async def get_hcp_profile(hcp_name: Optional[str] = None, hcp_id: Optional[int] = None) -> str:
    """Get the full profile of an HCP including their last 5 interactions.

    Args:
        hcp_name: The name of the HCP to look up.
        hcp_id: The ID of the HCP to look up. Either name or ID must be provided.
    """
    try:
        async with async_session_factory() as session:
            if hcp_id:
                stmt = select(HCP).where(HCP.id == hcp_id)
            elif hcp_name:
                stmt = select(HCP).where(HCP.name.ilike(f"%{hcp_name}%"))
            else:
                return json.dumps({
                    "success": False,
                    "message": "Please provide either an HCP name or ID.",
                })

            result = await session.execute(stmt)
            hcp = result.scalar_one_or_none()

            if not hcp:
                return json.dumps({
                    "success": False,
                    "message": f"HCP not found with {'name: ' + hcp_name if hcp_name else 'ID: ' + str(hcp_id)}.",
                })

            # Fetch last 5 interactions
            interactions_stmt = (
                select(Interaction)
                .where(Interaction.hcp_id == hcp.id)
                .order_by(Interaction.date.desc())
                .limit(5)
            )
            interactions_result = await session.execute(interactions_stmt)
            interactions = interactions_result.scalars().all()

            interactions_data = []
            for i in interactions:
                interactions_data.append({
                    "id": i.id,
                    "type": i.interaction_type,
                    "date": str(i.date),
                    "topics": i.topics_discussed,
                    "sentiment": i.sentiment,
                    "outcome": i.outcome,
                    "location": i.location,
                })

            return json.dumps({
                "success": True,
                "profile": {
                    "id": hcp.id,
                    "name": hcp.name,
                    "specialty": hcp.specialty,
                    "institution": hcp.institution,
                    "email": hcp.email,
                    "phone": hcp.phone,
                    "location": hcp.location,
                },
                "recent_interactions": interactions_data,
                "total_interactions": len(interactions_data),
            })

    except Exception as e:
        logger.error(f"Error in get_hcp_profile tool: {e}")
        return json.dumps({
            "success": False,
            "message": f"Error fetching HCP profile: {str(e)}",
        })
