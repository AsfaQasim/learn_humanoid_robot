from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import os
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import your RAG service functionality
from rag_service import RAGService

# Create FastAPI app
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Configure CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
    # Allow specific headers if needed
    # allow_headers=["Content-Type", "Authorization"],
)

# Initialize the RAG service
rag_service = None

@app.on_event("startup")
async def startup_event():
    global rag_service
    try:
        rag_service = RAGService()
        print("RAG Service initialized successfully")
    except Exception as e:
        print(f"Error initializing RAG Service: {e}")

@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    Chat endpoint that handles queries from the React frontend
    Expects: {
        "session_id": "123",
        "query_text": "what is physical ai",
        "collection_name": "my_embed"  # optional, defaults to "my_embed"
    }
    Returns: {"answer": "...", "sources": [...]}
    """
    global rag_service

    if not rag_service:
        raise HTTPException(status_code=500, detail="RAG Service not initialized")

    try:
        # Get raw JSON data from request
        raw_body = await request.json()
        print(f"Received request body: {raw_body}")  # Debugging

        # Extract query_text as the primary query field (as specified in requirements)
        user_query = raw_body.get("query_text")

        if not user_query:
            # Fallback to other possible field names, including the old "query" field
            user_query = (
                raw_body.get("query") or  # Support old format as fallback
                raw_body.get("message") or
                raw_body.get("question") or
                raw_body.get("prompt") or
                raw_body.get("text") or
                raw_body.get("input") or
                raw_body.get("user_message")
            )

        if not user_query:
            # Try to find any field that might contain the query
            for key, value in raw_body.items():
                if isinstance(value, str) and len(value.strip()) > 0:
                    user_query = value
                    print(f"Using '{key}' field as query: {user_query[:50]}...")
                    break

        if not user_query:
            raise HTTPException(status_code=400, detail="Query field is required. Expected 'query_text', 'query', 'message', 'question', 'prompt', 'text', 'input', or 'user_message' in request body")

        # Extract collection name with default fallback
        collection_name = raw_body.get("collection_name", "document_embeddings")  # Default collection

        print(f"Processing query: {user_query[:100]}...")  # Debugging
        print(f"Using collection: {collection_name}")  # Debugging

        # Process the user query using your RAG service with the specified collection
        # Note: We'll need to update the RAGService to accept collection name
        result = rag_service.query(user_query, top_k=5, collection_name=collection_name)

        # Format response to match frontend expectations
        return {
            "answer": result.get("response", "I couldn't process your request at the moment."),
            "sources": [chunk.get("content", "") for chunk in result.get("retrieved_chunks", [])],
            "query": user_query
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error processing request: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)