import json
import logging
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.agent.graph import agent_graph
from app.agent.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()


class ConversationMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_history: list[ConversationMessage] = []


class ChatResponse(BaseModel):
    response: str
    interaction_id: Optional[int] = None
    tools_used: list[str] = []
    suggested_follow_ups: list[str] = []
    extracted_fields: Optional[dict] = None
    partial_update: Optional[dict] = None


@router.post("/agent/chat", summary="Chat with AI agent", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):
    """Send a message to the AI agent for interaction logging and management."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail={"message": "Message cannot be empty."})

    try:
        # Build messages list from conversation history
        today_str = datetime.date.today().isoformat()
        current_system_prompt = SYSTEM_PROMPT.format(today=today_str)
        messages = [SystemMessage(content=current_system_prompt)]

        for msg in request.conversation_history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))

        # Add the new user message
        messages.append(HumanMessage(content=request.message))

        # Invoke the graph
        initial_state = {
            "messages": messages,
            "current_hcp_id": None,
            "interaction_draft": None,
            "tool_output": None,
            "suggested_followups": [],
        }

        result = await agent_graph.ainvoke(initial_state)

        # Extract response from the last AI message
        response_text = ""
        interaction_id = None
        tools_used = []
        suggested_follow_ups = []
        extracted_fields = None
        partial_update = None

        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tools_used.append(tc["name"])

            if hasattr(msg, "name") and msg.name:
                # This is a ToolMessage — parse for interaction_id, extracted/updated fields and suggestions
                try:
                    tool_data = json.loads(msg.content)
                    if tool_data.get("interaction_id"):
                        interaction_id = tool_data["interaction_id"]
                    if tool_data.get("suggested_follow_ups"):
                        suggested_follow_ups = tool_data["suggested_follow_ups"]
                    if tool_data.get("extracted_fields"):
                        extracted_fields = tool_data["extracted_fields"]
                    if tool_data.get("partial_update"):
                        partial_update = tool_data["partial_update"]
                except (json.JSONDecodeError, TypeError):
                    pass

        # Get the final AI response (last AIMessage without tool_calls)
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and not (hasattr(msg, "tool_calls") and msg.tool_calls):
                response_text = msg.content
                break

        if not response_text:
            response_text = "I processed your request. Please check the results."

        # Enforce Response Formatting Rules as a safety net
        if "log_interaction" in tools_used:
            if not response_text.startswith("Interaction logged successfully."):
                response_text = f"Interaction logged successfully. ID: {interaction_id or 'unknown'}\n\n{response_text}"
        elif "edit_interaction" in tools_used:
            if not response_text.startswith("Interaction updated successfully."):
                response_text = f"Interaction updated successfully. ID: {interaction_id or 'unknown'}\n\n{response_text}"
        elif "schedule_follow_up" in tools_used:
            # We don't overwrite if it looks like the LLM already formatted it correctly, 
            # but if it has "Interaction logged", we definitely clean it up.
            if "Interaction logged successfully" in response_text:
                # Most likely the LLM hallucinated the prefix, we'll try to use the Tool outcome directly or clean it.
                response_text = response_text.replace("Interaction logged successfully.", "Follow-up scheduled successfully.")
        elif "get_hcp_profile" in tools_used or "summarize_interactions" in tools_used:
            # Strip any accidental "Interaction logged successfully" prefix
            if "Interaction logged successfully" in response_text:
                lines = response_text.split('\n')
                filter_lines = [l for l in lines if "Interaction logged successfully" not in l and "ID:" not in l]
                response_text = '\n'.join(filter_lines).strip()

        return ChatResponse(
            response=response_text.strip(),
            interaction_id=interaction_id,
            tools_used=list(set(tools_used)),
            suggested_follow_ups=suggested_follow_ups,
            extracted_fields=extracted_fields,
            partial_update=partial_update,
        )

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Agent chat error: {error_msg}")

        if "unavailable" in error_msg.lower() or "rate" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail={"message": "AI service temporarily unavailable. Please try again in a moment."},
            )

        raise HTTPException(
            status_code=500,
            detail={"message": f"Agent execution failed: {error_msg}"},
        )
