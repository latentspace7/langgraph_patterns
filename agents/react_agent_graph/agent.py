from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from agents.react_agent_graph.utils.nodes import math_agent, tools


graph = StateGraph(MessagesState)

# Add nodes
graph.add_node("math_agent", math_agent)
graph.add_node("math_tool", ToolNode(tools))

# Edges - workflow
graph.add_edge(START, "math_agent")

# if the model made tool calls -> go to ToolNode; else -> END
graph.add_conditional_edges(
    "math_agent",
    tools_condition,
    {"tools": "math_tool", END: END},
)

graph.add_edge("math_tool", "math_agent")

math_agent_graph = graph.compile()
