"""
RAG Service module that provides chat functionality
compatible with the existing agent implementation in agent.py
Designed for serverless environments
"""
import os
import logging
from typing import List, Dict, Any, Optional, Set
import threading

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

import cohere
import google.generativeai as genai
from qdrant_client import QdrantClient
import sys
import os
# Add backend directory to path for relative imports when running directly
backend_dir = os.path.dirname(__file__)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from qdrant_compat import safe_qdrant_search

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


class RAGService:
    """RAG Service class that provides chat functionality optimized for serverless environments."""

    # Class-level cache for clients to reuse across instances when possible
    _cohere_client = None
    _gemini_model = None
    _qdrant_client = None
    _available_collections = set()
    _lock = threading.Lock()  # Thread-safe initialization

    def __init__(self):
        # Initialize clients on demand per instance for serverless
        self.cohere_client = self._get_cohere_client()
        self.gemini_model = self._get_gemini_model()
        self.qdrant = self._get_qdrant_client()

    @classmethod
    def _get_cohere_client(cls):
        """Get or create a Cohere client."""
        if not cls._cohere_client:
            with cls._lock:
                if not cls._cohere_client:
                    cls._cohere_client = cohere.Client(COHERE_API_KEY)
        return cls._cohere_client

    @classmethod
    def _get_gemini_model(cls):
        """Get or create a Gemini model."""
        if cls._gemini_model is None:
            with cls._lock:
                if cls._gemini_model is None:
                    if GEMINI_API_KEY and len(GEMINI_API_KEY) > 10:
                        try:
                            genai.configure(api_key=GEMINI_API_KEY)
                            cls._gemini_model = genai.GenerativeModel("gemini-2.5-flash")
                            logger.info("Gemini model initialized successfully")
                        except Exception as e:
                            logger.warning(f"Gemini initialization failed, will use Cohere for chat: {e}")
                            cls._gemini_model = None
                    else:
                        logger.info("No Gemini API key found, will use Cohere for chat generation")
        return cls._gemini_model

    @classmethod
    def _get_qdrant_client(cls):
        """Get or create a Qdrant client."""
        if cls._qdrant_client is None:
            with cls._lock:
                if cls._qdrant_client is None:
                    try:
                        logger.info("=" * 60)
                        logger.info("INITIALIZING QDRANT WITH COMPATIBILITY LAYER - VERSION 2.0")
                        logger.info("=" * 60)
                        cls._qdrant_client = QdrantClient(
                            url=QDRANT_URL,
                            api_key=QDRANT_API_KEY,
                            https=True
                        )
                        collections_response = cls._qdrant_client.get_collections()
                        cls._available_collections = {col.name for col in collections_response.collections}
                        logger.info(f"Connected to Qdrant Cloud. Available collections: {cls._available_collections}")
                    except Exception as e:
                        logger.error(f"Could not connect to Qdrant Cloud at {QDRANT_URL}: {e}")
                        cls._qdrant_client = None
        return cls._qdrant_client


    def refresh_available_collections(self) -> Set[str]:
        """Refresh the list of available collections from Qdrant."""
        if self.qdrant is None:
            return set()
        try:
            collections_response = self.qdrant.get_collections()
            self._available_collections = {col.name for col in collections_response.collections}
            logger.debug(f"Refreshed collections: {self._available_collections}")
        except Exception as e:
            logger.warning(f"Failed to refresh collections: {e}")
        return self._available_collections


    def get_safe_collection_name(self, requested_collection: str) -> str:
        """
        Validate and return a safe collection name.
        Falls back to DEFAULT_COLLECTION_NAME if requested collection doesn't exist.

        Args:
            requested_collection: The collection name requested by the client

        Returns:
            A valid collection name that exists in Qdrant
        """
        if not requested_collection:
            logger.warning("Empty collection name received, using default")
            return DEFAULT_COLLECTION_NAME

        if requested_collection in self._available_collections:
            return requested_collection

        self.refresh_available_collections()

        if requested_collection in self._available_collections:
            return requested_collection

        logger.warning(
            f"Collection '{requested_collection}' not found in Qdrant. "
            f"Available: {self._available_collections}. Falling back to '{DEFAULT_COLLECTION_NAME}'"
        )

        if DEFAULT_COLLECTION_NAME in self._available_collections:
            return DEFAULT_COLLECTION_NAME

        if self._available_collections:
            fallback = next(iter(self._available_collections))
            logger.warning(f"Default collection not found. Using first available: '{fallback}'")
            return fallback

        logger.error("No collections available in Qdrant")
        return DEFAULT_COLLECTION_NAME


    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings using Cohere's embedding API."""
        try:
            response = self.cohere_client.embed(
                texts=[text],
                model="embed-english-v3.0",  # Use instance variable
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding with Cohere: {e}")
            raise


    def retrieve_docs(self, query: str, top_k: int = 5, collection_name: str = DEFAULT_COLLECTION_NAME) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from Qdrant.
        Automatically falls back to valid collection if requested one doesn't exist.
        """
        if self.qdrant is None:
            logger.error("Qdrant client is not initialized. Cannot retrieve documents.")
            return []

        safe_collection = self.get_safe_collection_name(collection_name)
        logger.info(f"Retrieving from collection: '{safe_collection}' (requested: '{collection_name}')")

        try:
            vector = self.embed_text(query)

            # Use compatibility layer to handle different Qdrant client versions
            results = safe_qdrant_search(
                client=self.qdrant,
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


    def build_prompt(self, question: str, context_docs: List[Dict[str, Any]]) -> str:
        """Build the prompt for the LLM with retrieved context."""
        context = "\n\n".join([doc["content"] for doc in context_docs])

        return f"""
You are a helpful AI assistant.
Use ONLY the context below to answer the question.
If the answer is not in the context, provide the best possible answer based on the available information.
Do NOT start your response with "I don't know", "I'm not sure", or "Based on my knowledge".
Be concise and helpful in your response.

Context:
{context}

Question:
{question}

Answer:
"""


    def _clean_llm_answer(self, text: str) -> str:
        """Remove accidental debug/metadata text from model output."""
        if not text or not isinstance(text, str):
            return ""

        t = text.strip()

        # If the model echoes a "Sources (...)" section, strip it from the answer.
        lower = t.lower()
        for marker in ["\nsources (", "\nsource (", "\nsources:", "\nsource:", "sources (", "sources:"]:
            idx = lower.find(marker)
            if idx != -1:
                t = t[:idx].rstrip()
                break

        # If the model dumps "Selected Text:" metadata, strip it too.
        lower = t.lower()
        idx = lower.find("selected text:")
        if idx != -1:
            t = t[:idx].rstrip()

        return t

    def _generate_response(self, prompt: str) -> str:
        """Generate response using available model (Gemini or Cohere)."""
        if self.gemini_model:
            response = self.gemini_model.generate_content(prompt)
            return self._clean_llm_answer(response.text)
        else:
            response = self.cohere_client.chat(
                message=prompt,
                model="command-a-03-2025"
            )
            return self._clean_llm_answer(response.text)

    def _validate_response_accuracy(self, response: str, context_docs: List[Dict[str, Any]]) -> bool:
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
        context_text = " ".join([doc["content"] for doc in context_docs]).lower()
        response_lower = response.lower()

        # Check if response contains key terms from context
        context_words = set(context_text.split()[:50])  # Take first 50 words as representative
        response_words = set(response_lower.split())

        # If at least some overlap exists, consider it grounded
        overlap = context_words.intersection(response_words)
        if len(overlap) > 0:
            # Check for invalid phrases even if there's overlap
            invalid_phrases = [
                "i don't know",
                "could not find",
                "not sure"
            ]

            for phrase in invalid_phrases:
                if response_lower.startswith(phrase) or phrase in response_lower:
                    return False

            return True

        return False


    def query(self, user_message: str, top_k: int = 5, collection_name: str = DEFAULT_COLLECTION_NAME) -> Dict[str, Any]:
        """
        Process a user query and return a response with retrieved context.
        Automatically uses a valid collection even if requested one doesn't exist.
        """
        try:
            safe_collection = self.get_safe_collection_name(collection_name)
            docs = self.retrieve_docs(user_message, top_k, safe_collection)

            if not docs:
                prompt = f"""
You are a helpful AI assistant. The user asked: "{user_message}"
I couldn't find relevant information in the knowledge base to answer this question.
Provide the best possible answer based on your general knowledge.
Do NOT start your response with "I don't know", "I'm not sure", or "Based on my knowledge".
Be helpful and informative in your response.
"""
                answer = self._generate_response(prompt)

                # Validate response accuracy even when no docs found
                is_accurate = self._validate_response_accuracy(answer, docs)

                return {
                    "response": answer,
                    "retrieved_chunks": [],
                    "query": user_message,
                    "collection_used": safe_collection,
                    "is_accurate": is_accurate,
                    "sources_tracked": []  # Track sources for reproducibility
                }

            prompt = self.build_prompt(user_message, docs)
            answer = self._generate_response(prompt)

            # Validate response accuracy against retrieved context
            is_accurate = self._validate_response_accuracy(answer, docs)

            # Track sources for reproducibility (constitution requirement)
            sources_tracked = [
                {
                    "content_snippet": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"],
                    "source_url": doc.get("source_url", ""),
                    "chapter": doc.get("chapter", ""),
                    "relevance_score": doc.get("relevance_score", 0.0)
                }
                for doc in docs
            ]

            return {
                "response": answer,
                "retrieved_chunks": docs,
                "query": user_message,
                "collection_used": safe_collection,
                "is_accurate": is_accurate,  # Constitution alignment for accuracy
                "sources_tracked": sources_tracked  # Constitution alignment for reproducibility
            }

        except Exception as e:
            import traceback
            logger.error(f"Error processing query: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            return {
                "response": f"Error processing your request: {str(e)}",
                "retrieved_chunks": [],
                "query": user_message,
                "collection_used": DEFAULT_COLLECTION_NAME,
                "is_accurate": False,
                "sources_tracked": []
            }
