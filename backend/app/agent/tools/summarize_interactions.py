import json
import logging
from typing import Optional

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from sqlalchemy import select

from app.database import async_session_factory
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.services.llm import get_secondary_llm, invoke_with_retry

logger = logging.getLogger(__name__)


@tool
async def summarize_interactions(hcp_name: Optional[str] = None, hcp_id: Optional[int] = None, count: int = 5) -> str:
    """Summarize recent interactions with an HCP.

    Args:
        hcp_name: The name of the HCP.
        hcp_id: The ID of the HCP. Either name or ID must be provided.
        count: Number of recent interactions to summarize (default 5).
    """
    try:
        count = min(max(int(count), 1), 20)  # Cap between 1 and 20
        async with async_session_factory() as session:
            # Find HCP
            if hcp_id:
                stmt = select(HCP).where(HCP.id == int(hcp_id))
            elif hcp_name:
                stmt = select(HCP).where(HCP.name.ilike(f"%{hcp_name}%"))
            else:
                return json.dumps({
                    "success": False,
                    "message": "Please provide either an HCP name or ID.",
                })

            result = await session.execute(stmt)
            # Use first() instead of scalar_one_or_none() to avoid MultipleResultsFound 
            # if multiple HCPs match the name.
            hcp = result.scalars().first()

            if not hcp:
                logger.error(f"Summarize tool: HCP lookup failed. hcp_name='{hcp_name}', hcp_id='{hcp_id}'")
                return json.dumps({
                    "success": False,
                    "message": f"HCP not found for name '{hcp_name}' or id '{hcp_id}'.",
                })

            # Fetch last N interactions
            interactions_stmt = (
                select(Interaction)
                .where(Interaction.hcp_id == hcp.id)
                .order_by(Interaction.date.desc())
                .limit(count)
            )
            interactions_result = await session.execute(interactions_stmt)
            interactions = interactions_result.scalars().all()
            
            logger.info(f"Summarize tool: HCP matched '{hcp.name}' (ID: {hcp.id}). Found {len(interactions)} interactions.")

            if not interactions:
                logger.warning(f"Summarize tool: No interactions found for HCP '{hcp.name}' (ID: {hcp.id}). Query count: {count}")
                return json.dumps({
                    "success": True,
                    "message": f"No interactions found for {hcp.name}.",
                    "summary": f"No recorded interactions with {hcp.name}.",
                })

            # Build interaction data for summarization
            interaction_texts = []
            for i in interactions:
                parts = [f"Date: {i.date}, Type: {i.interaction_type}"]
                parts.append(f"Topics: {i.topics_discussed or 'Not recorded'}")
                parts.append(f"Sentiment: {i.sentiment or 'Not recorded'}")
                parts.append(f"Outcome: {i.outcome or 'Not recorded'}")
                if i.materials_shared:
                    parts.append(f"Materials: {', '.join(i.materials_shared)}")
                interaction_texts.append(" | ".join(parts))

            interaction_data = "\n".join(interaction_texts)

            # Use secondary (larger) LLM for summarization
            llm = get_secondary_llm()
            summary_prompt = f"""Summarize the following {len(interactions)} recent interactions with {hcp.name} ({hcp.specialty} at {hcp.institution}) into a concise paragraph. Focus on key themes, sentiment trends, outcomes, and any action items.

Interactions:
{interaction_data}

Provide a professional, concise summary paragraph:"""

            response = await invoke_with_retry(llm, [HumanMessage(content=summary_prompt)])

            return json.dumps({
                "success": True,
                "hcp_name": hcp.name,
                "interactions_count": len(interactions),
                "summary": response.content.strip(),
                "agent_instruction": "Display this summary directly to the user. DO NOT say that no interactions are logged, and DO NOT ask them to log an interaction. Just provide the summary."
            })

    except Exception as e:
        logger.error(f"Error in summarize_interactions tool: {e}")
        return json.dumps({
            "success": False,
            "message": f"Error summarizing interactions: {str(e)}",
        })
