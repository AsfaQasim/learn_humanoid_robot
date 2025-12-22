from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..services.rag_service import RAGService
from ..vector_store import get_qdrant_client
from ..config import DEFAULT_COLLECTION_NAME
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    query_text: str
    collection_name: str = DEFAULT_COLLECTION_NAME  # Use configured default collection
    selected_text: str | None = None

class ChatResponse(BaseModel):
    response_id: str
    response_text: str
    sources: List[str]

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Initialize RAG service with Qdrant client
        qdrant_client = get_qdrant_client()
        rag_service = RAGService(qdrant_client=qdrant_client)

        # Retrieve relevant documents from Qdrant
        retrieved_docs = rag_service.retrieve(
            query=request.query_text,
            collection_name=request.collection_name,
            selected_text=request.selected_text,
            top_k=5  # Retrieve top 5 relevant documents
        )

        # Generate response using Gemini
        response_text = rag_service.generate_response(
            query=request.query_text,
            retrieved_docs=retrieved_docs
        )

        return ChatResponse(
            response_id=str(uuid.uuid4()),
            response_text=response_text,
            sources=retrieved_docs  # Include the retrieved documents as sources
        )
    except Exception as e:
        import traceback
        error_msg = str(e)
        logger.error(f"Chat error: {error_msg}\nTraceback: {traceback.format_exc()}")

        # Check if it's a quota error and provide specific messaging
        if "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "429" in error_msg:
            return ChatResponse(
                response_id=str(uuid.uuid4()),
                response_text="The chat service is currently experiencing high demand. Please try again later or check your API quota settings.",
                sources=[]
            )
        elif "model" in error_msg.lower() and ("not found" in error_msg.lower() or "404" in error_msg.lower()):
            return ChatResponse(
                response_id=str(uuid.uuid4()),
                response_text="The AI model configuration is incorrect. Please contact the administrator to check the model settings.",
                sources=[]
            )
        elif "embedding" in error_msg.lower() or "connection" in error_msg.lower():
            # Handle embedding model connection issues
            return ChatResponse(
                response_id=str(uuid.uuid4()),
                response_text="I'm having trouble connecting to my knowledge base right now. Please try again in a moment.",
                sources=[]
            )
        else:
            # Return generic error response for other exceptions
            return ChatResponse(
                response_id=str(uuid.uuid4()),
                response_text=f"I encountered an issue processing your request. Please try again or ask your question in a different way.",
                sources=[]
            )
