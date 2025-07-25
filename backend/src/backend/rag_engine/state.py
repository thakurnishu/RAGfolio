from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    llm: Runnable
    next_step: str | None
