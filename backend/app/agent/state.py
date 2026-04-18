from typing import TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """State for the LangGraph agent."""

    messages: Annotated[list[BaseMessage], operator.add]
    current_hcp_id: Optional[int]
    interaction_draft: Optional[dict]
    tool_output: Optional[dict]
    suggested_followups: list[str]
