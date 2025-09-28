from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from agents.supervisor_agent.sub_agents.math_agent import math_agent
from agents.supervisor_agent.sub_agents.research_agent import top_ai_posts
from agents.supervisor_agent.sub_agents.mcp_agent import mcp_agent


mcp_agent = mcp_agent()

supervisor = create_supervisor(
    model=init_chat_model("anthropic:claude-3-7-sonnet-latest"),
    agents=[top_ai_posts, math_agent, mcp_agent],
    prompt=(
        "You are a supervisor agent. You do not perform tasks yourself; "
        "instead you decide which sub-agent to call. You have access to these tools:\n\n"
        "- math_agent: handles basic arithmetic, numeric calculations, and simple quantitative reasoning.\n"
        "- top_ai_posts: fetches AI-related posts and news, including top 5 items, summaries, and links.\n"
        "- mcp_agent: connects to an MCP server and executes MCP tool calls.\n\n"
        "When a user asks something, select the most appropriate tool and hand off the request."
    ),
    add_handoff_back_messages=False,
    output_mode="full_history",
).compile()
