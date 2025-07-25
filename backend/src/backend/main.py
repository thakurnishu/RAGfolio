from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from backend.rag_engine.agent_caller import call_llm

from dotenv import load_dotenv
load_dotenv()

class RequestState(BaseModel):
    user_query: str

class ResponseState(BaseModel):
    ai_response: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    yield

app = FastAPI(
        title="RAGfolio",
        lifespan=lifespan
)

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
async def rag_query_endpoint(request: RequestState):
    """API Endpoint to ask for qurey related to User's Resume"""

    ai_response = await call_llm(request.user_query)

    return ResponseState(ai_response=ai_response)
