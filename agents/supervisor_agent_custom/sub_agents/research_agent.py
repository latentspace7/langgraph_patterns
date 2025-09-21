from langgraph.prebuilt import create_react_agent
from agents.supervisor_agent.sub_agents.utils.tools import sing_lullaby

prompt = (
    "IMPORTANT: You must ONLY use the provided sing_lullaby tool. Do NOT use any built-in web search capabilities.\n"
    "Accept the results from sing_lullaby as complete and final - do not seek additional information.\n"
    "- Only use the sing_lullaby tool for your work, do NOT make up any URLs."
)


lullaby = create_react_agent(
    model="claude-3-7-sonnet-latest",
    tools=[sing_lullaby],
    prompt=prompt,
    name="lullaby",
)
