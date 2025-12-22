from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from ..vector_store import get_qdrant_client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class RAGService:
    def __init__(self, qdrant_client: QdrantClient = None, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.qdrant_client = qdrant_client or get_qdrant_client()
        self.embedding_model_name = embedding_model_name
        self._embedding_model = None  # Lazy load the model

    @property
    def embedding_model(self):
        """Lazy load the embedding model to handle connection issues"""
        if self._embedding_model is None:
            try:
                # Set timeout and retry settings for the model
                import huggingface_hub
                # Reduce backoff time to avoid long waits
                huggingface_hub.utils._http.BACKOFF_MAX = 2
                # Set connection timeout
                import requests
                from sentence_transformers import SentenceTransformer
                import os
                os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'  # Disable hf_transfer which can cause issues

                self._embedding_model = SentenceTransformer(
                    self.embedding_model_name,
                    cache_folder="./model_cache",  # Use local cache
                    trust_remote_code=True  # In case the model needs it
                )
                logger.info(f"Successfully loaded embedding model: {self.embedding_model_name}")
            except Exception as e:
                logger.error(f"Error loading embedding model: {e}")
                # If loading fails, we'll try to handle queries differently
                # Let's try with a fallback approach or handle gracefully
                self._embedding_model = None
                raise e
        return self._embedding_model

    def retrieve(self, query: str, collection_name: str, selected_text: str | None = None, top_k: int = 5) -> list:
        """
        Retrieves relevant documents from the Qdrant collection.

        Args:
            query (str): The user's query.
            collection_name (str): The name of the Qdrant collection.
            selected_text (str, optional): The user-selected text. Defaults to None.
            top_k (int, optional): The number of documents to retrieve. Defaults to 5.

        Returns:
            list: A list of retrieved documents.
        """
        try:
            if selected_text:
                query = f"{selected_text}\n\n{query}"

            # Enhance query for robotics/AI related searches
            enhanced_query = self._enhance_query(query)

            # Check if embedding model is loaded, if not try to load it
            if self._embedding_model is None:
                try:
                    _ = self.embedding_model  # This will trigger loading
                except Exception as load_error:
                    logger.error(f"Failed to load embedding model: {load_error}")
                    return []  # Return empty list if model can't be loaded

            query_embedding = self.embedding_model.encode(enhanced_query)
            search_result = self.qdrant_client.query_points(
                collection_name=collection_name,
                query=query_embedding.tolist(),
                limit=top_k,
                with_payload=True
            )

            # Filter out empty or very short documents and deduplicate
            retrieved_texts = []
            seen_texts = set()
            for hit in search_result.points:
                text = hit.payload["text"]
                if text and len(text.strip()) > 10 and text not in seen_texts:  # Filter out very short texts
                    retrieved_texts.append(text)
                    seen_texts.add(text)

            return retrieved_texts
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            # Return empty list if retrieval fails, which will trigger the out-of-context response
            return []

    def _enhance_query(self, query: str) -> str:
        """
        Enhance the query to improve retrieval for robotics/AI related topics.
        """
        query_lower = query.lower()

        # Check if query is related to robotics or AI
        robotics_keywords = ['robot', 'robotics', 'ai', 'artificial intelligence', 'machine learning',
                           'deep learning', 'neural network', 'automation', 'humanoid', 'physical ai',
                           'sensors', 'actuators', 'locomotion', 'manipulation', 'control system']

        # If it's robotics/AI related, enhance the query with related terms
        if any(keyword in query_lower for keyword in robotics_keywords):
            enhanced_query = f"{query} robotics artificial intelligence machine learning humanoid automation"
            return enhanced_query

        return query

    def generate_response(self, query: str, retrieved_docs: list) -> str:
        """
        Generates a response using the retrieved documents and the user's query.

        Args:
            query (str): The user's query.
            retrieved_docs (list): A list of retrieved documents.

        Returns:
            str: The generated response.
        """
        # Check if the query is a greeting (only if it's purely a greeting without content questions)
        query_lower = query.lower().strip()
        greeting_keywords = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']

        # Only treat as greeting if it's a simple greeting without additional content
        is_pure_greeting = any(keyword == query_lower for keyword in greeting_keywords)
        is_greeting_with_question = any(keyword in query_lower for keyword in greeting_keywords) and ('?' in query or 'what' in query or 'how' in query or 'tell me' in query or 'about' in query)

        if is_pure_greeting and not is_greeting_with_question:
            return "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant. I can help you with questions about robotics, AI, physical computing, and related topics. What would you like to know about the textbook content?"

        # Check if we have relevant context
        if not retrieved_docs or len([doc for doc in retrieved_docs if doc.strip()]) == 0:
            # No context found, respond appropriately
            if "book" in query_lower or "textbook" in query_lower or "robotics" in query_lower:
                return "I'm your Physical AI & Humanoid Robotics textbook assistant. The textbook contains information about robotics, AI, physical computing, and related topics. Please ask specific questions about the content, and I'll do my best to help you based on the available information."
            else:
                # Out of context but not about the book, provide general response
                return f"Your question '{query}' seems interesting, but it's not part of the textbook context. I'm specifically designed to assist with the Physical AI & Humanoid Robotics textbook content. Please ask questions related to robotics, AI, or the textbook topics, and I'll be happy to help!"
        else:
            # We have context, use it
            context = "\n".join(retrieved_docs)

            # Check if query is robotics/AI related to customize the prompt
            robotics_related = any(keyword in query_lower for keyword in
                                 ['robot', 'robotics', 'ai', 'artificial intelligence', 'machine learning',
                                  'humanoid', 'physical ai', 'automation', 'ros', 'urdf'])

            if robotics_related:
                prompt = f"""You are an expert assistant for a Physical AI & Humanoid Robotics textbook.
The user is asking about robotics and AI topics from the textbook.

Context from the textbook (these are relevant excerpts):
{context}

User's question: {query}

Please provide a detailed, comprehensive answer based on the textbook context.
If the context contains information about robotics, AI, ROS, URDF, Python agents,
or related topics, use that information to answer the question thoroughly. Include specific concepts,
definitions, and examples from the context when relevant.
Structure your response with:
1. A clear answer based on the context
2. Specific concepts or techniques mentioned in the context
3. Any relevant examples from the textbook
If the information is not available in the context, acknowledge this limitation
but provide general knowledge about the topic if possible."""
            else:
                prompt = f"""You are a helpful assistant for a Physical AI & Humanoid Robotics textbook.

Context from the textbook:
{context}

Question: {query}

Answer: If the question is about Physical AI, Humanoid Robotics, ROS, URDF, or related topics, answer based on the context. If the question is out of context or about general topics not related to robotics/AI, politely explain that the information is not in the provided context but you can provide general information about it."""

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=800,  # Increased to allow for more detailed responses
                    temperature=0.6,  # Slightly lower temperature for more focused responses
                ),
                # Add request options for timeout handling
                request_options={"timeout": 45}  # Increased timeout
            )
            return response.text.strip()
        except Exception as gemini_error:
            logger.error(f"Gemini API error: {gemini_error}")
            # Fallback response using just the context
            fallback_response = f"Based on the textbook content:\n\n{context[:500]}..."
            return fallback_response
