from fastapi import FastAPI
from backend.rag_engine.agent import call_llm

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from your RAG backend!"}

@app.get("/rag_query")
def rag_query():
    return call_llm()
