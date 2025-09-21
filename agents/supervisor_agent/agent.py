from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from agents.supervisor_agent.sub_agents.math_agent import math_agent
from agents.supervisor_agent.sub_agents.research_agent import lullaby

supervisor = create_supervisor(
    model=init_chat_model("anthropic:claude-3-7-sonnet-latest"),
    agents=[lullaby, math_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()
