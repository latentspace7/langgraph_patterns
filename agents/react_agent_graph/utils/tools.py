from langchain_core.tools import tool


@tool
def add(a: float, b: float):
    """Add two numbers."""
    return a + b


@tool
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: float, b: float):
    """Divide two numbers."""
    return a / b
