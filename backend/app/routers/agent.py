import json
import logging
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

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

        # Invoke the graph with manual loop control and circuit breaker
        initial_state = {
            "messages": messages,
            "current_hcp_id": None,
            "interaction_draft": None,
            "tool_output": None,
            "suggested_followups": [],
        }
        
        steps = 0
        result = initial_state
        
        # We use astream to monitor and control the execution flow
        async for state in agent_graph.astream(
            initial_state, 
            stream_mode="values", 
            config={"recursion_limit": 10}
        ):
            steps += 1
            result = state
            
            messages = state.get("messages", [])
            if not messages:
                continue
                
            last_msg = messages[-1]
            
            # Fix 1: Disable Tool Chaining
            # If we just received a tool result, and the agent tries to call another tool, we stop.
            # A normal flow is: Human -> AI (Tool) -> Tool (Result) -> AI (Response)
            # If it goes: Human -> AI (Tool) -> Tool (Result) -> AI (Tool) ... we stop at the second AI (Tool).
            if len(messages) >= 3:
                tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
                if tool_messages and isinstance(last_msg, AIMessage) and last_msg.tool_calls:
                    logger.warning("Tool chaining detected in router. Forcing stop to prevent infinite loop.")
                    break

            # Fix 2: Circuit Breaker
            if steps >= 5:
                logger.warning(f"Circuit breaker fired: reached {steps} steps. Forcing termination.")
                break

        # Extract response from the last AI message
        response_text = ""
        interaction_id = None
        tools_used = []
        suggested_follow_ups = []
        extracted_fields = None
        partial_update = None

        tool_summary_text = None

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
                    if tool_data.get("summary"):
                        tool_summary_text = tool_data["summary"]
                        logger.info(f"Extracting summary: {tool_summary_text[:50]}...")
                except (json.JSONDecodeError, TypeError):
                    logger.error(f"Failed to parse tool message: {msg.content}")

        # Get the final AI response (last AIMessage without tool_calls)
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and not (hasattr(msg, "tool_calls") and msg.tool_calls):
                response_text = msg.content
                break

        if not response_text:
            response_text = "I processed your request. Please check the results."

        logger.info(f"Response text: {response_text}. Tool summary: {tool_summary_text}")
        
        # Fix 1: Build response directly from tool output to eliminate hallucinations
        if "get_hcp_profile" in tools_used:
            # We already have profile/interactions in tool_data if successful
            # Reconstruct a clean profile presentation
            for msg in result["messages"]:
                if isinstance(msg, ToolMessage) and msg.name == "get_hcp_profile":
                    try:
                        data = json.loads(msg.content)
                        if data.get("success"):
                            p = data["profile"]
                            response_text = f"Profile for {p['name']} ({p['specialty']})\n"
                            response_text += f"Institution: {p['institution']}\n"
                            response_text += f"Location: {p['location']}\n"
                            response_text += f"Contact: {p['email']} | {p['phone']}\n\n"
                            
                            if data.get("recent_interactions"):
                                response_text += "Recent Interactions:\n"
                                for i in data["recent_interactions"]:
                                    response_text += f"- {i['date']}: {i['type']} ({i['outcome']})\n"
                            else:
                                response_text += "No recent interactions found."
                        else:
                            response_text = data.get("message", "Failed to retrieve profile.")
                    except:
                        pass
                    break

        elif "log_interaction" in tools_used:
            response_text = f"Interaction logged successfully. ID: {interaction_id or 'unknown'}"
            if suggested_follow_ups:
                response_text += "\n\nSuggested Follow-ups:\n" + "\n".join([f"- {s}" for s in suggested_follow_ups])

        elif "edit_interaction" in tools_used:
            response_text = f"Interaction updated successfully. ID: {interaction_id or 'unknown'}"

        elif "schedule_follow_up" in tools_used:
            # Try to find tool output for name and date
            tool_msg_found = False
            for msg in result["messages"]:
                if isinstance(msg, ToolMessage) and msg.name == "schedule_follow_up":
                    try:
                        data = json.loads(msg.content)
                        if data.get("success"):
                            hcp_name_tool = data.get("hcp_name", "HCP")
                            follow_up_date = data.get("follow_up_date", "specified date")
                            response_text = f"Follow-up scheduled successfully for {hcp_name_tool} on {follow_up_date}."
                            tool_msg_found = True
                        else:
                            response_text = data.get("message", "Failed to schedule follow-up.")
                            tool_msg_found = True
                    except:
                        pass
                    break
            if not tool_msg_found:
                response_text = "I attempted to schedule the follow-up, but could not confirm the details. Please check the follow-up list."

        elif "summarize_interactions" in tools_used:
            if tool_summary_text:
                response_text = tool_summary_text
            else:
                for msg in result["messages"]:
                    if isinstance(msg, ToolMessage) and msg.name == "summarize_interactions":
                        try:
                            data = json.loads(msg.content)
                            response_text = data.get("summary", response_text)
                        except:
                            pass

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
