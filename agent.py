import os
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# CONFIG
# =========================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# HARD-CODED collection name - ignore frontend collection_name
HARDCODED_COLLECTION_NAME = "my_embed"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # set in env

# Validate required environment variables
if not QDRANT_URL:
    raise ValueError("[ERROR] QDRANT_URL environment variable not set")
if not QDRANT_API_KEY:
    raise ValueError("[ERROR] QDRANT_API_KEY environment variable not set")
if not GEMINI_API_KEY:
    raise ValueError("[ERROR] GEMINI_API_KEY environment variable not set")

# =========================
# SERVERLESS INIT
# =========================

# Create FastAPI app without global initialization for serverless compatibility
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
        "https://*.vercel.app",   # Vercel deployments
        os.getenv("FRONTEND_URL", ""),  # Environment-specific URL
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# =========================
# SCHEMAS
# =========================

class ChatRequest(BaseModel):
    session_id: str
    query_text: str
    collection_name: str = None  # This will be ignored

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    is_accurate: bool = True
    sources_tracked: List[Dict[str, Any]] = []

# =========================
# HELPERS
# =========================

def embed_text(text: str, api_key: str):
    """Generate embeddings using Google's embedding API with error handling"""
    try:
        # Configure API for this request
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")

        # Use the embedding API to generate embeddings
        result = genai.embed_content(
            model="models/embedding-001",  # Gemini embedding model
            content=text,
            task_type="retrieval_query"  # or "retrieval_document", "semantic_similarity", etc.
        )
        return result['embedding']
    except Exception as e:
        error_msg = str(e).lower()
        if "embed_content_free_tier_requests" in error_msg or "quota" in error_msg or "rate limit" in error_msg:
            raise Exception("Embedding quota exceeded. Please try again later.")
        else:
            raise Exception(f"Error generating embedding: {e}")

def retrieve_docs(query: str, top_k: int = 5, qdrant_url: str = None, qdrant_api_key: str = None, collection_name: str = None):
    """Retrieve documents from Qdrant with error handling - serverless compatible"""
    try:
        # Initialize Qdrant client for this request
        qdrant = QdrantClient(
            url=qdrant_url or QDRANT_URL,
            api_key=qdrant_api_key or QDRANT_API_KEY,
            https=True
        )

        vector = embed_text(query, GEMINI_API_KEY)

        # Use HARD-CODED collection name, ignore any collection_name from frontend
        collection = collection_name or HARDCODED_COLLECTION_NAME
        results = qdrant.search(
            collection_name=collection,
            query_vector=vector,
            limit=top_k,
            with_payload=True
        )

        docs = []
        sources_tracked = []
        for r in results:
            payload = r.payload or {}
            content = payload.get("text") or payload.get("content", "")
            if content:
                docs.append(content)
                # Track sources for reproducibility
                sources_tracked.append({
                    "content_snippet": content[:100] + "..." if len(content) > 100 else content,
                    "source_url": payload.get("source_url", payload.get("url", "")),
                    "chapter": payload.get("chapter", payload.get("section", payload.get("title", ""))),
                    "relevance_score": float(r.score)
                })

        return docs, sources_tracked
    except UnexpectedResponse as e:
        if e.status_code == 404:
            # Collection doesn't exist - return empty results gracefully
            logger.warning(f"Collection '{HARDCODED_COLLECTION_NAME}' does not exist: {e}")
            return [], []
        else:
            logger.error(f"Qdrant error: {e}")
            raise Exception(f"Qdrant error: {e}")
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise Exception(f"Error retrieving documents: {e}")

def build_prompt(question: str, context_docs: List[str]) -> str:
    context = "\n\n".join(context_docs)

    return f"""
You are a helpful AI assistant.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know".
Be concise and helpful in your response.

Context:
{context}

Question:
{question}

Answer:
"""

def validate_response_accuracy(response: str, context_docs: List[str]) -> bool:
    """
    Validate that the response is grounded in the provided context.
    This addresses the constitution requirement for 'Accuracy'.
    """
    if not context_docs:
        # If no context was provided, any response claiming lack of info is valid
        if "I don't know" in response or "couldn't find" in response.lower():
            return True
        return False

    # Simple validation: check if response contains information from context
    context_text = " ".join(context_docs).lower()
    response_lower = response.lower()

    # Check if response contains key terms from context
    context_words = set(context_text.split()[:50])  # Take first 50 words as representative
    response_words = set(response_lower.split())

    # If at least some overlap exists, consider it grounded
    overlap = context_words.intersection(response_words)
    if len(overlap) > 0:
        return True

    # Additional check: if response admits lack of information, it's valid
    if "i don't know" in response_lower or "could not find" in response_lower or "no information" in response_lower:
        return True

    return False

# =========================
# API
# =========================

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request):
    """
    Chat endpoint that handles queries from the React frontend
    Expects: {
        "session_id": "123",
        "query_text": "what is physical ai",
        "collection_name": "ignored"  # This is ignored, hardcoded to my_embed
    }
    Returns: {"answer": "...", "sources": [...]}
    """
    try:
        # Get raw JSON data from request
        raw_body = await request.json()
        logger.info(f"Received request with keys: {list(raw_body.keys())}")

        # Extract query_text as the primary query field
        user_query = raw_body.get("query_text")

        if not user_query:
            # Fallback to other possible field names
            user_query = (
                raw_body.get("query") or
                raw_body.get("message") or
                raw_body.get("question") or
                raw_body.get("prompt") or
                raw_body.get("text") or
                raw_body.get("input") or
                raw_body.get("user_message")
            )

        if not user_query:
            raise HTTPException(status_code=400, detail="Query field is required")

        # IGNORE frontend collection_name - use hardcoded collection
        # Any collection_name from frontend is ignored
        collection_name = HARDCODED_COLLECTION_NAME

        # Retrieve relevant documents using the hardcoded collection
        docs, sources_tracked = retrieve_docs(user_query, top_k=5)

        if not docs:
            return ChatResponse(
                answer="No data found in knowledge base",
                sources=[],
                is_accurate=True,  # Accurate because it correctly reports no data
                sources_tracked=[]
            )

        prompt = build_prompt(user_query, docs)

        # Configure and use Gemini model for this request
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model_for_request = genai.GenerativeModel("gemini-2.5-flash")
        response = gemini_model_for_request.generate_content(prompt)

        answer = response.text.strip()

        # Validate response accuracy
        is_accurate = validate_response_accuracy(answer, docs)

        return ChatResponse(
            answer=answer,
            sources=docs,
            is_accurate=is_accurate,
            sources_tracked=sources_tracked
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing request: {error_msg}")
        if "quota" in error_msg.lower() or "embed_content_free_tier_requests" in error_msg.lower():
            return ChatResponse(
                answer="Embedding quota exceeded. Please try again later.",
                sources=[],
                is_accurate=False,
                sources_tracked=[]
            )
        else:
            return ChatResponse(
                answer="Error processing your request. Please try again later.",
                sources=[],
                is_accurate=False,
                sources_tracked=[]
            )

@app.get("/health")
def health():
    return {"status": "healthy", "model": "gemini-2.5-flash", "serverless": True}

# For Vercel serverless functions - no uvicorn needed