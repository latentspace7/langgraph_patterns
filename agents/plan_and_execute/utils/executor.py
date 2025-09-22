from langgraph.prebuilt import create_react_agent
from agents.plan_and_execute.utils.tools import reverse_string
from dotenv import load_dotenv

load_dotenv()

executor = create_react_agent(
    model="claude-sonnet-4-20250514",
    tools=[reverse_string],
    name="executor",
)
