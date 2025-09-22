from langgraph.graph import MessagesState
from typing import Annotated, List, Tuple
import operator


class PlanExecute(MessagesState):
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str
