import json
import logging
from langchain_core.messages import AIMessage, ToolMessage

from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import ALL_TOOLS
from app.services.llm import get_primary_llm, invoke_with_retry

logger = logging.getLogger(__name__)


async def agent_node(state: AgentState) -> dict:
    """Agent node that calls the LLM with tools bound.

    The LLM decides whether to call a tool or respond directly.
    """
    llm = get_primary_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    messages = state["messages"]

    response = await invoke_with_retry(llm_with_tools, messages)

    return {"messages": [response]}


async def tool_node(state: AgentState) -> dict:
    """Tool node that executes the tool selected by the agent.

    Processes tool calls from the last AI message and returns tool results.
    """
    messages = state["messages"]
    last_message = messages[-1]

    tool_results = []
    tools_by_name = {tool.name: tool for tool in ALL_TOOLS}

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

            if tool_name in tools_by_name:
                try:
                    result = await tools_by_name[tool_name].ainvoke(tool_args)
                    tool_results.append(
                        ToolMessage(
                            content=str(result),
                            tool_call_id=tool_call["id"],
                            name=tool_name,
                        )
                    )
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    tool_results.append(
                        ToolMessage(
                            content=json.dumps({"error": str(e)}),
                            tool_call_id=tool_call["id"],
                            name=tool_name,
                        )
                    )
            else:
                tool_results.append(
                    ToolMessage(
                        content=json.dumps({"error": f"Unknown tool: {tool_name}"}),
                        tool_call_id=tool_call["id"],
                        name=tool_name,
                    )
                )

    return {"messages": tool_results}
