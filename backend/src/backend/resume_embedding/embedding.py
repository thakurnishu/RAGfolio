import os

from langchain_chroma.vectorstores import Chroma
from backend.resume_embedding.config import ResumeConfig
from backend.resume_embedding.embedding_system import ResumeEmbeddingSystem

async def start_embedding() -> Chroma:
    resume_config = ResumeConfig()

    resume_file_path = f"{os.getcwd()}/resume.pdf"

    embedding_pipeline = ResumeEmbeddingSystem(resume_config)

    # Load Document
    docs = embedding_pipeline.load_resume_document(resume_file_path)

    # Chunk it
    chucks = embedding_pipeline.chunk_documents(docs)

    # Store in ChromaDB
    _ = embedding_pipeline.store_in_chromadb(chunks=chucks)

    return embedding_pipeline.vectorstore
