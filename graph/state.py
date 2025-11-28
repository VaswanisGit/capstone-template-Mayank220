# Graph State
from typing import TypedDict, Annotated, List, Union
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[Union[str, dict]], add_messages]
    # Add other state variables here
