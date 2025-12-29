"""
RAG Service module that provides chat functionality
compatible with the existing agent implementation in agent.py
"""
import os
import logging
from typing import List, Dict, Any, Optional, Set

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

import cohere
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_compat import safe_qdrant_search

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
DEFAULT_COLLECTION_NAME = "document_embeddings"
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not QDRANT_URL:
    raise ValueError("QDRANT_URL environment variable not set")
if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY environment variable not set")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set")


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    response: str
    retrieved_chunks: List[Dict[str, Any]] = []
    query: str


cohere_client = cohere.Client(COHERE_API_KEY)
COHERE_EMBED_MODEL = "embed-english-v3.0"

gemini_model = None
if GEMINI_API_KEY and len(GEMINI_API_KEY) > 10:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        # Test the model
        gemini_model.generate_content("test")
        logger.info("Gemini model initialized successfully")
    except Exception as e:
        logger.warning(f"Gemini initialization failed, using Cohere for chat: {e}")
        gemini_model = None
else:
    logger.info("No Gemini API key found, using Cohere for chat generation")

qdrant: Optional[QdrantClient] = None
available_collections: Set[str] = set()

try:
    logger.info("=" * 60)
    logger.info("INITIALIZING QDRANT WITH COMPATIBILITY LAYER - VERSION 2.0")
    logger.info("=" * 60)
    qdrant = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        https=True
    )
    collections_response = qdrant.get_collections()
    available_collections = {col.name for col in collections_response.collections}
    logger.info(f"Connected to Qdrant Cloud. Available collections: {available_collections}")
except Exception as e:
    logger.error(f"Could not connect to Qdrant Cloud at {QDRANT_URL}: {e}")
    qdrant = None


def refresh_available_collections() -> Set[str]:
    """Refresh the list of available collections from Qdrant."""
    global available_collections
    if qdrant is None:
        return set()
    try:
        collections_response = qdrant.get_collections()
        available_collections = {col.name for col in collections_response.collections}
        logger.debug(f"Refreshed collections: {available_collections}")
    except Exception as e:
        logger.warning(f"Failed to refresh collections: {e}")
    return available_collections


def get_safe_collection_name(requested_collection: str) -> str:
    """
    Validate and return a safe collection name.
    Falls back to DEFAULT_COLLECTION_NAME if requested collection doesn't exist.

    Args:
        requested_collection: The collection name requested by the client

    Returns:
        A valid collection name that exists in Qdrant
    """
    global available_collections

    if not requested_collection:
        logger.warning("Empty collection name received, using default")
        return DEFAULT_COLLECTION_NAME

    if requested_collection in available_collections:
        return requested_collection

    refresh_available_collections()

    if requested_collection in available_collections:
        return requested_collection

    logger.warning(
        f"Collection '{requested_collection}' not found in Qdrant. "
        f"Available: {available_collections}. Falling back to '{DEFAULT_COLLECTION_NAME}'"
    )

    if DEFAULT_COLLECTION_NAME in available_collections:
        return DEFAULT_COLLECTION_NAME

    if available_collections:
        fallback = next(iter(available_collections))
        logger.warning(f"Default collection not found. Using first available: '{fallback}'")
        return fallback

    logger.error("No collections available in Qdrant")
    return DEFAULT_COLLECTION_NAME


def embed_text(text: str) -> List[float]:
    """Generate embeddings using Cohere's embedding API."""
    try:
        response = cohere_client.embed(
            texts=[text],
            model=COHERE_EMBED_MODEL,
            input_type="search_query"
        )
        return response.embeddings[0]
    except Exception as e:
        logger.error(f"Error generating embedding with Cohere: {e}")
        raise


def retrieve_docs(query: str, top_k: int = 5, collection_name: str = DEFAULT_COLLECTION_NAME) -> List[Dict[str, Any]]:
    """
    Retrieve relevant documents from Qdrant.
    Automatically falls back to valid collection if requested one doesn't exist.
    """
    global qdrant

    if qdrant is None:
        logger.error("Qdrant client is not initialized. Cannot retrieve documents.")
        return []

    safe_collection = get_safe_collection_name(collection_name)
    logger.info(f"Retrieving from collection: '{safe_collection}' (requested: '{collection_name}')")

    try:
        vector = embed_text(query)

        # Use compatibility layer to handle different Qdrant client versions
        results = safe_qdrant_search(
            client=qdrant,
            collection_name=safe_collection,
            query_vector=vector,
            limit=top_k,
            with_payload=True
        )

        docs = []
        for r in results:
            payload = r.payload or {}

            # Debug: log payload keys to understand data structure
            logger.debug(f"Payload keys: {list(payload.keys())}")

            # Try multiple possible field names for content
            content = (
                payload.get("text") or
                payload.get("content") or
                payload.get("page_content") or
                payload.get("body") or
                payload.get("description") or
                ""
            )
            source_url = payload.get("source_url", payload.get("url", ""))
            chapter = payload.get("chapter", payload.get("section", payload.get("title", "")))

            # Only add documents that have actual content (not raw metadata)
            if content and isinstance(content, str) and len(content.strip()) > 10:
                # Clean content - remove any metadata artifacts
                clean_content = content.strip()
                docs.append({
                    "content": clean_content,
                    "source_url": source_url,
                    "chapter": chapter,
                    "relevance_score": r.score
                })

        logger.info(f"Retrieved {len(docs)} documents from '{safe_collection}'")
        return docs

    except Exception as e:
        logger.error(f"Error retrieving documents from Qdrant: {e}")
        return []


def build_prompt(question: str, context_docs: List[Dict[str, Any]]) -> str:
    """Build the prompt for the LLM with retrieved context."""
    context = "\n\n".join([doc["content"] for doc in context_docs])

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


class RAGService:
    """RAG Service class that provides chat functionality."""

    def __init__(self):
        self.gemini_model = gemini_model
        self.cohere_client = cohere_client
        self.qdrant = qdrant

    def _generate_response(self, prompt: str) -> str:
        """Generate response using available model (Gemini or Cohere)."""
        if self.gemini_model:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        else:
            response = self.cohere_client.chat(
                message=prompt,
                model="command-a-03-2025"
            )
            return response.text.strip()

    def query(self, user_message: str, top_k: int = 5, collection_name: str = DEFAULT_COLLECTION_NAME) -> Dict[str, Any]:
        """
        Process a user query and return a response with retrieved context.
        Automatically uses a valid collection even if requested one doesn't exist.
        """
        try:
            safe_collection = get_safe_collection_name(collection_name)
            docs = retrieve_docs(user_message, top_k, safe_collection)

            if not docs:
                prompt = f"""
You are a helpful AI assistant. The user asked: "{user_message}"
I couldn't find relevant information in the knowledge base to answer this question.
You can still try to provide a helpful response based on general knowledge,
but please acknowledge that you're not using specific context from the knowledge base.
"""
                answer = self._generate_response(prompt)

                return {
                    "response": answer,
                    "retrieved_chunks": [],
                    "query": user_message,
                    "collection_used": safe_collection
                }

            prompt = build_prompt(user_message, docs)
            answer = self._generate_response(prompt)

            return {
                "response": answer,
                "retrieved_chunks": docs,
                "query": user_message,
                "collection_used": safe_collection
            }

        except Exception as e:
            import traceback
            logger.error(f"Error processing query: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            return {
                "response": f"Error processing your request: {str(e)}",
                "retrieved_chunks": [],
                "query": user_message,
                "collection_used": DEFAULT_COLLECTION_NAME
            }
