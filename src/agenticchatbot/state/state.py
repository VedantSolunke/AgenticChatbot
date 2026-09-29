from typing import Any
from typing_extensions import Annotated, NotRequired, TypedDict, List
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represents the state of the chatbot, including user input and messages.
    """
    messages: Annotated[List, add_messages]
    frequency: NotRequired[str]
    news_data: NotRequired[List[dict[str, Any]]]
    summary: NotRequired[str]
    filename: NotRequired[str]
    saved: NotRequired[bool]