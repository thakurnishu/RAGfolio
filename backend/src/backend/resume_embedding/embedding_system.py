from typing import Any, Dict, List

from backend.resume_embedding.config import ResumeConfig
from langchain_core.documents.base import Document as langchain_docs
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import uuid

class ResumeEmbeddingSystem:
    def __init__(self, config: ResumeConfig):
        self.config = config
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001"
        )
        self.vectorstore =  Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embeddings
        )        
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_resume_document(self, file_path: str) -> List[langchain_docs]:
        """Load resume from file (supports txt, pdf)"""

        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata.update({
                'source': file_path,
                'type': 'resume',
                'timestamp': str(uuid.uuid4())
            })
        
        return documents
    
    def chunk_documents(self, documents: List[langchain_docs]) -> List[langchain_docs]:
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        
        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                'chunk_id': i,
                'chunk_size': len(chunk.page_content)
            })
        
        return chunks
    
    def store_in_chromadb(self, chunks: List[langchain_docs], user_id: str = "default_user") -> List[str]:
        """Store chunks and embeddings in ChromaDB with override capability"""
        # First, delete existing resume for this user
        self._delete_existing_resume(user_id)
        
        ids = []
        docs = []
        
        # Add user_id to metadata for tracking
        for chunk in chunks:
            metadata = chunk.metadata.copy()
            metadata.update({
                'user_id': user_id,
                'is_current': True,
                'stored_at': str(uuid.uuid4())  # Using UUID as timestamp placeholder
            })
            docs.append(langchain_docs(page_content=chunk.page_content, metadata=metadata))
            ids.append(str(uuid.uuid4()))
        
        self.vectorstore.add_documents(documents=docs, ids=ids)
        return ids
    
    def _delete_existing_resume(self, user_id: str = "default_user"):
        """Delete existing resume chunks for a user"""

        # Retrieve existing documents via raw access
        existing = self.vectorstore._collection.get(where={"user_id": user_id})
        ids = existing.get("ids", [])
        if ids:
            print(f"Deleting {len(ids)} existing chunks for user {user_id}")
            self.vectorstore.delete(ids=ids)
        else:
            print(f"No existing chunks to delete for user {user_id}")
    
    def get_resume_info(self, user_id: str = "default_user") -> Dict[str, Any]:
        """Get information about stored resume"""

        existing = self.vectorstore._collection.get(where={"user_id": user_id}, include=["metadatas"])
        ids = existing.get("ids", [])
        metas = existing.get("metadatas", [])
        if ids:
            sample = metas[0] if metas else {}
            return {
                "user_id": user_id,
                "total_chunks": len(ids),
                "source": sample.get("source", "Unknown"),
                "type": sample.get("type", "Unknown"),
                "stored_at": sample.get("stored_at", "Unknown")
            }
        return {"user_id": user_id, "status": "No resume found"}
