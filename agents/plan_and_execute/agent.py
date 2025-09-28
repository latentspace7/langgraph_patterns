from agents.plan_and_execute.utils.nodes import (
    execute_step,
    plan_step,
    replan_step,
)
from agents.plan_and_execute.utils.executor import executor as agent_executor
from agents.plan_and_execute.utils.state import PlanExecute
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage


def should_end(state: PlanExecute):
    if "response" in state and state["response"]:
        return END
    else:
        return "agent"


def tools_condition(state: PlanExecute):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls"):
        return "tools"
    else:
        return END


def call_tools(state: PlanExecute):
    return {"messages": [agent_executor.invoke({"messages": state["messages"]})]}


workflow = StateGraph(PlanExecute)

# Add the plan node
workflow.add_node("planner", plan_step)

# Add the execution step
workflow.add_node("agent", execute_step)

# Add a replan node
workflow.add_node("replan", replan_step)

# Add the tools node
workflow.add_node("tools", call_tools)

workflow.add_edge(START, "planner")

# From plan we go to agent
workflow.add_edge("planner", "agent")

# From agent, we replan
workflow.add_edge("agent", "replan")

workflow.add_conditional_edges(
    "replan",
    # Determine which node is called next.
    should_end,
    ["agent", END],
)

workflow.add_conditional_edges(
    "agent",
    # Determine which node is called next.
    tools_condition,
    ["tools", END],
)


# Compile to a Runnable
plan_and_execute = workflow.compile(name="plan_and_execute")

