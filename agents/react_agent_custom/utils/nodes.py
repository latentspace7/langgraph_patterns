from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model
from agents.react_agent_custom.utils.tools import add, multiply, divide

# tools
tools = [add, multiply, divide]

# LLM bound to tools
llm = init_chat_model("anthropic:claude-3-7-sonnet-latest", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# agent node: call the model on the running message list


def math_agent(state: MessagesState):
    # state["messages"] is maintained by MessagesState reducer
    msg = llm_with_tools.invoke(state["messages"])
    # return partial state update
    return {"messages": [msg]}
