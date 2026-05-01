import logging
from langgraph.graph import StateGraph, END
from langchain_core.messages import ToolMessage

from app.agent.state import AgentState
from app.agent.nodes import agent_node, tool_node

logger = logging.getLogger(__name__)


def should_continue(state: AgentState) -> str:
    """Determine whether to continue to tool_node or end.

    If the last message has tool calls, route to tool_node.
    Otherwise, route to END.
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Safety break: count tool messages in the current run
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
    if len(tool_messages) > 5:
        logger.warning("Safety break: Too many tool calls detected. Ending graph execution.")
        return END

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool_node"
    return END


def build_graph():
    """Build the LangGraph StateGraph for the agent.

    Graph structure:
    agent_node -> (if tool call) -> tool_node -> agent_node
    agent_node -> (if no tool call) -> END
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent_node", agent_node)
    graph.add_node("tool_node", tool_node)

    # Set entry point
    graph.set_entry_point("agent_node")

    # Add conditional edge from agent_node
    graph.add_conditional_edges(
        "agent_node",
        should_continue,
        {
            "tool_node": "tool_node",
            END: END,
        },
    )

    # Tool node always routes back to agent_node
    graph.add_edge("tool_node", "agent_node")

    return graph.compile()


# Compile the graph at module level for reuse
agent_graph = build_graph()
