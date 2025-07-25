from langchain_core.tools import tool
from backend.rag_engine.embedding import start_embedding
from backend.resume_embedding.embedding_system import ResumeEmbeddingSystem

@tool
def add(a: int, b: int):
    """Adds two numbers."""
    return a + b + 2


@tool
async def portfolio_retrieval(query: str, user_id: str = "default_user"):
    """Search resume content using semantic similarity for specific user"""

    vector_datastore = await start_embedding()

    retriever = vector_datastore.as_retriever(
            search_kwargs={"k": 5},
            search_type="similarity",
            filter={"user_id": user_id}
    )
    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information on it."

    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")
    
    return "\n\n".join(results)

tools = [add, portfolio_retrieval]
