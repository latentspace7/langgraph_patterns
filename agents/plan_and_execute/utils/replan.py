from typing import Union
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from agents.plan_and_execute.utils.plan import Plan
from langgraph.prebuilt import create_react_agent


class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


# replanner_prompt = ChatPromptTemplate.from_template(
#     """For the given objective, come up with a simple step by step plan. \
# This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
# The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

# Your objective was this:
# {input}

# Your original plan was this:
# {plan}

# You have currently done the follow steps:
# {past_steps}

# Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""
# )

replanner_prompt = ChatPromptTemplate.from_messages([
    ("system", """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Based on the conversation history, determine if you need to update the plan or if you can provide a final response.

If the task is complete, use Response to provide the final answer.
If more steps are needed, use Plan to provide the remaining steps."""),
    ("placeholder", "{messages}")
])


# replanner_prompt = ChatPromptTemplate.from_messages([
#     ("system", """For the given objective, come up with a simple step by step plan. \
# This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
# The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

# Based on the conversation history, determine if you need to update the plan or if you can provide a final response."""),
#     ("placeholder", "{messages}")
# ])


chat_llm = init_chat_model("claude-sonnet-4-20250514", temperature=0)
replanner = replanner_prompt | chat_llm.with_structured_output(Act)
