from langgraph.prebuilt import create_react_agent
from agents.supervisor_agent.sub_agents.utils.tools import fetch_top_ai_posts

prompt = (
    "IMPORTANT:\n"
    "- You must ONLY use the provided **fetch_top_ai_posts** tool.\n"
    "- NEVER use any built-in web search, browsing, or external retrieval capabilities.\n"
    "- Do NOT fabricate or imagine URLs, articles, or sources.\n"
    "- Treat the results returned by **fetch_top_ai_posts** as the single, complete, and final source of truth.\n"
    "- If the tool does not provide information, clearly state that no results are available — do not attempt to supplement from elsewhere.\n"
)


top_ai_posts = create_react_agent(
    model="claude-3-7-sonnet-latest",
    tools=[fetch_top_ai_posts],
    prompt=prompt,
    name="top_ai_posts",
)
