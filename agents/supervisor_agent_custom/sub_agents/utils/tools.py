from langchain_core.tools import tool


@tool
def sing_lullaby(query: str) -> str:
    """Format string as comprehensive web search results."""
    if not query or query.strip() == "":
        return "Please provide a valid search query."

    result = f"Ok Ill  sing you a lullaby of {query}."
    return result
