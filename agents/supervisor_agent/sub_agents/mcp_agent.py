# mcp_agent.py
import asyncio
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from pathlib import Path


async def _load_mcp_tools():

    SERVER_PATH = (Path(__file__).parent / "server.py").resolve()
    print(f"Using MCP server at: {SERVER_PATH}")

    client = MultiServerMCPClient({
        "local": {
            "transport": "stdio",
            "command": "python",
            "args": [str(SERVER_PATH)],
            # "transport": "streamable_http", "url": "http://localhost:3000/mcp/",
        }
    })
    return await client.get_tools()


def mcp_agent():
    tools = asyncio.run(_load_mcp_tools())

    llm = init_chat_model("anthropic:claude-3-7-sonnet-latest", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    def agent(state: MessagesState):
        msg = llm_with_tools.invoke(state["messages"])
        return {"messages": [msg]}

    sg = StateGraph(MessagesState)
    sg.add_node("agent", agent)
    sg.add_node("tools", ToolNode(tools))
    sg.add_edge(START, "agent")
    sg.add_conditional_edges("agent", tools_condition, {
                             "tools": "tools", END: END})
    sg.add_edge("tools", "agent")
    return sg.compile(name="mcp_agent")
