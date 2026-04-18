import json
import logging
from typing import Optional

from langchain_core.tools import tool
from sqlalchemy import select

from app.database import async_session_factory
from app.models.interaction import Interaction

logger = logging.getLogger(__name__)


@tool
async def edit_interaction(interaction_id: int, updates: str) -> str:
    """Edit an existing interaction record.

    Args:
        interaction_id: The ID of the interaction to update.
        updates: JSON string of fields to update. Example: '{"outcome": "New outcome text", "sentiment": "positive"}'
    """
    try:
        # Parse updates
        if isinstance(updates, str):
            update_dict = json.loads(updates)
        else:
            update_dict = updates

        async with async_session_factory() as session:
            stmt = select(Interaction).where(Interaction.id == interaction_id)
            result = await session.execute(stmt)
            interaction = result.scalar_one_or_none()

            if not interaction:
                return json.dumps({
                    "success": False,
                    "message": f"Interaction with ID {interaction_id} not found.",
                })

            # Apply updates
            partial_update = {}
            for key, value in update_dict.items():
                if hasattr(interaction, key) and key not in ("id", "created_at", "hcp_id"):
                    setattr(interaction, key, value)
                    partial_update[key] = value

            await session.commit()

            return json.dumps({
                "success": True,
                "interaction_id": interaction_id,
                "message": f"Successfully updated interaction {interaction_id}. Updated fields: {', '.join(partial_update.keys())}.",
                "partial_update": partial_update,
            })

    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "message": "Invalid update format. Please provide valid field names and values.",
        })
    except Exception as e:
        logger.error(f"Error in edit_interaction tool: {e}")
        return json.dumps({
            "success": False,
            "message": f"Error updating interaction: {str(e)}",
        })
