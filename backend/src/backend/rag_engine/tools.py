from langchain_chroma.vectorstores import Chroma
from langchain_core.tools import tool

@tool
def add(a: int, b: int):
    """Adds two numbers."""
    return a + b + 2


def create_portfolio_retrieval(vector_datastore: Chroma):
    @tool
    def portfolio_retrieval(query: str, user_id: str = "default_user"):
        """Search resume content using semantic similarity for specific user"""

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
    return portfolio_retrieval

tools = [add]
