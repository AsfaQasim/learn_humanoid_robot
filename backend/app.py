import os
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import logging

from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    response_id: str
    feedback: int

# Load environment variables - skip .env file in serverless environments
import os
if os.environ.get("VERCEL") != "1":
    # Only load .env file locally, not in Vercel
    from dotenv import load_dotenv
    load_dotenv()

# Import your RAG service functionality
import sys
import os
# Add current directory to path for relative imports
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from rag_service import RAGService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0",
    docs_url=None,  # Disable docs in production for security
    redoc_url=None  # Disable redoc in production for security
)

# Configure CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://localhost:3001",  # Alternative React dev server
        "http://localhost:8000",  # Same origin for direct access
        "https://*.vercel.app",   # Vercel deployments
        os.getenv("FRONTEND_URL", ""),  # Environment-specific URL
        "http://localhost:*",     # Allow any localhost port during development
        "https://localhost:*",    # Allow HTTPS localhost during development
        "*"  # Allow all origins during development - remove in production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly specify methods
    allow_headers=["*"],  # Allow all headers
    # Additional CORS options for better compatibility
    allow_origin_regex=r"https?://(?:.+\.)?localhost(?::\d+)?",  # Regex for localhost variations
)

@app.options("/chat")
async def chat_options(request: Request):
    """Handle preflight OPTIONS requests for CORS"""
    return {"status": "OK"}

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
    try:
        # Get raw JSON data from request
        raw_body = await request.json()
        logger.info(f"Received request with keys: {list(raw_body.keys())}")
        logger.info(f"Received request path: {request.url.path}")

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
                    logger.info(f"Using '{key}' field as query: {user_query[:50]}...")
                    break

        if not user_query:
            raise HTTPException(status_code=400, detail="Query field is required. Expected 'query_text', 'query', 'message', 'question', 'prompt', 'text', 'input', or 'user_message' in request body")

        # Extract collection name with default fallback
        collection_name = raw_body.get("collection_name", "document_embeddings")  # Default collection

        logger.info(f"Processing query: {user_query[:100]}...")
        logger.info(f"Using collection: {collection_name}")

        # Check if required environment variables are set
        if not os.getenv("QDRANT_URL") or not os.getenv("QDRANT_API_KEY") or not os.getenv("COHERE_API_KEY"):
            # Return a helpful error message if environment variables are not set
            return {
                "response_id": str(uuid.uuid4()),
                "answer": "The chatbot is not properly configured. Please set the required environment variables (QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY) in the backend/.env file.",
                "sources": [],
                "query": user_query,
                "collection_used": collection_name
            }

        # Initialize RAG service for each request in serverless environment
        try:
            rag_service = RAGService()
        except Exception as init_error:
            logger.error(f"Error initializing RAG Service: {init_error}")
            logger.error(f"Environment variables available: QDRANT_URL set: {bool(os.getenv('QDRANT_URL'))}, QDRANT_API_KEY set: {bool(os.getenv('QDRANT_API_KEY'))}, COHERE_API_KEY set: {bool(os.getenv('COHERE_API_KEY'))}")
            # Return a more user-friendly error message instead of throwing an exception
            return {
                "response_id": str(uuid.uuid4()),
                "answer": f"The chatbot service is temporarily unavailable: {str(init_error)}",
                "sources": [],
                "query": user_query,
                "collection_used": collection_name
            }

        # Process the user query using your RAG service with the specified collection
        result = rag_service.query(user_query, top_k=5, collection_name=collection_name)

        response_id = str(uuid.uuid4())

        # Format response to match frontend expectations
        return {
            "response_id": response_id,
            "answer": result.get("response", "I couldn't process your request at the moment."),
            "sources": [chunk.get("content", "") for chunk in result.get("retrieved_chunks", [])],
            "query": user_query,
            "collection_used": result.get("collection_used", collection_name)
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(f"Full traceback: ", exc_info=True)  # Log full traceback for debugging
        # Return a more user-friendly error message instead of throwing an exception
        return {
            "response_id": str(uuid.uuid4()),
            "answer": f"An error occurred while processing your request: {str(e)}",
            "sources": [],
            "query": user_query,
            "collection_used": raw_body.get("collection_name", "document_embeddings")
        }

@app.post("/feedback")
async def feedback_endpoint(feedback: FeedbackRequest):
    """Accept simple thumbs-up/down feedback from the frontend."""
    if feedback.feedback not in (-1, 1):
        raise HTTPException(status_code=400, detail="feedback must be 1 or -1")

    # Minimal implementation: log feedback. Persisting to DB can be added later.
    logger.info(f"Feedback received: response_id={feedback.response_id} feedback={feedback.feedback}")

    return {"ok": True}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "serverless": True}

# For Vercel serverless functions
# The app instance is all that's needed - no need for uvicorn in serverless