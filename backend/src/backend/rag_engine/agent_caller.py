from typing import Sequence, cast
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.human import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.rag_engine.embedding import start_embedding
from backend.rag_engine.state import AgentState
from backend.rag_engine.workflow import compile_graph_state
from backend.rag_engine.tools import create_portfolio_retrieval
from backend.rag_engine.tools import tools


async def call_llm(rag_query: str):

    vector_store = await start_embedding()

    portfolio_retrieval = create_portfolio_retrieval(vector_store)
    tools.append(portfolio_retrieval)
    
    model = "gemini-2.5-flash"
    llm = ChatGoogleGenerativeAI(model=model).bind_tools(tools)

    compile_agent = compile_graph_state()

    agent_input = AgentState({
        "messages": cast(Sequence[BaseMessage], [HumanMessage(content=rag_query)]),
        "llm": llm,
        "next_step": None
    })

    response = compile_agent.invoke(agent_input)

    return response["messages"][-1].content
