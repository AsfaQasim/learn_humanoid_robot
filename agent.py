import os
from typing import List
import logging

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
# INIT
# =========================

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize Qdrant client with cloud configuration
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    https=True
)

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Configure CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
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

# =========================
# HELPERS
# =========================

def embed_text(text: str):
    """Generate embeddings using Google's embedding API with error handling"""
    try:
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

def retrieve_docs(query: str, top_k: int = 5):
    """Retrieve documents from Qdrant with error handling"""
    try:
        vector = embed_text(query)

        # Use HARD-CODED collection name, ignore any collection_name from frontend
        results = qdrant.search(
            collection_name=HARDCODED_COLLECTION_NAME,
            query_vector=vector,
            limit=top_k,
            with_payload=True
        )

        docs = []
        for r in results:
            payload = r.payload or {}
            content = payload.get("text") or payload.get("content", "")
            if content:
                docs.append(content)

        return docs
    except UnexpectedResponse as e:
        if e.status_code == 404:
            # Collection doesn't exist - return empty results gracefully
            print(f"Collection '{HARDCODED_COLLECTION_NAME}' does not exist: {e}")
            return []
        else:
            print(f"Qdrant error: {e}")
            raise Exception(f"Qdrant error: {e}")
    except Exception as e:
        print(f"Error retrieving documents: {e}")
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
        docs = retrieve_docs(user_query, top_k=5)

        if not docs:
            return ChatResponse(
                answer="No data found in knowledge base",
                sources=[]
            )

        prompt = build_prompt(user_query, docs)

        response = gemini_model.generate_content(prompt)

        answer = response.text.strip()

        return ChatResponse(
            answer=answer,
            sources=docs
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "embed_content_free_tier_requests" in error_msg.lower():
            return ChatResponse(
                answer="Embedding quota exceeded. Please try again later.",
                sources=[]
            )
        else:
            print(f"Error processing request: {error_msg}")
            return ChatResponse(
                answer="Error processing your request. Please try again later.",
                sources=[]
            )

@app.get("/health")
def health():
    return {"status": "healthy", "model": "gemini-2.5-flash"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)