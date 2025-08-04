from datetime import datetime, timezone
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from backend.rag_engine.agent_caller import call_llm

from dotenv import load_dotenv

from backend.resume_embedding.embedding import start_embedding
load_dotenv()

class RequestState(BaseModel):
    user_query: str

class ResponseState(BaseModel):
    ai_response: str

vector_store = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global vector_store
    print("🚀 Starting up: Loading vector store...")
    vector_store = await start_embedding()
    print("✅ Vector store loaded successfully")
    yield

app = FastAPI(
        title="RAGfolio",
        lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_vector_store():
    """Dependency to provide vector store to route handlers"""
    global vector_store
    if vector_store is None:
        raise Exception("Vector store not initialized")
    return vector_store

@app.get("/healthz")
def health_check():
    """ Health check endpoint that returns the service status. """

    return JSONResponse(
        content={
            "server_status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        status_code=200,
    )

@app.post("/rag_query")
async def rag_query_endpoint(
        request: RequestState,
        vector_store=Depends(get_vector_store)
):
    """API Endpoint to ask for qurey related to User's Resume"""

    ai_response = await call_llm(request.user_query, vector_store)
    #ai_response = await call_llm(request.user_query)
    return ResponseState(ai_response=ai_response)
