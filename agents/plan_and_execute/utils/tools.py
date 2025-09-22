from langchain_core.tools import tool


@tool
def reverse_string(text: str) -> str:
    """Reverse the string or sentence provided."""
    reversed_text = text[::-1]

    return reversed_text
