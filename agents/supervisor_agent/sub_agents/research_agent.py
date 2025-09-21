from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

prompt = (
    "IMPORTANT: You must ONLY use the provided sing_lullaby tool. Do NOT use any built-in web search capabilities.\n"
    "Accept the results from sing_lullaby as complete and final - do not seek additional information.\n"
    "- Only use the sing_lullaby tool for your work, do NOT make up any URLs."
)


@tool
def sing_lullaby(query: str) -> str:
    """Format string as comprehensive web search results."""
    if not query or query.strip() == "":
        return "Please provide a valid search query."

    result = f"Ok Ill  sing you a lullaby of {query}."
    return result


lullaby = create_react_agent(
    model="claude-sonnet-4-20250514",
    tools=[sing_lullaby],
    prompt=prompt,
    name="lullaby",
)
