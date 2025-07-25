from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    message: Annotated[Sequence[BaseMessage], add_messages]
    llm: Runnable


def call_llm():
    model = "gemini-2.5-flash"

    llm = ChatGoogleGenerativeAI(model=model) 
    return "llm is running" 
