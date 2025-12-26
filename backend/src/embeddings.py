"""
Embedding generation module for the RAG ingestion pipeline.
Handles generating vector representations using Cohere API.
"""

import cohere
from typing import List, Dict
import time
import random
from .models.data_models import DocumentChunk, VectorRepresentation
from .config import config
from .errors import EmbeddingError, RateLimitError, ConfigurationError
from .logging_config import logger
from .utils import get_current_timestamp


class EmbeddingGenerator:
    """Handles generating embeddings for text chunks using Cohere API."""

    def __init__(self):
        """Initialize the embedding generator with Cohere client."""
        if not config.COHERE_API_KEY:
            raise ConfigurationError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(config.COHERE_API_KEY)
        self.model = "embed-english-v3.0"  # Using Cohere's latest embedding model

    def generate_embeddings(self, chunks: List[DocumentChunk], max_retries: int = 3) -> List[VectorRepresentation]:
        """
        Generate embeddings for a list of document chunks with retry logic.

        Args:
            chunks: List of DocumentChunk objects to generate embeddings for
            max_retries: Maximum number of retry attempts

        Returns:
            List of VectorRepresentation objects
        """
        if not chunks:
            logger.warning("No chunks provided for embedding generation")
            return []

        logger.info(f"Generating embeddings for {len(chunks)} chunks")

        # Extract text content from chunks
        texts = [chunk.content for chunk in chunks]

        # Try to generate embeddings with retry logic
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                # Generate embeddings using Cohere
                response = self.client.embed(
                    texts=texts,
                    model=self.model,
                    input_type="search_document"  # Optimize for search use case
                )

                embeddings = response.embeddings
                vectors = []

                # Create VectorRepresentation objects
                for i, embedding_vector in enumerate(embeddings):
                    chunk = chunks[i]

                    vector_repr = VectorRepresentation(
                        id="",
                        vector=embedding_vector,
                        chunk_id=chunk.id,
                        model_used=self.model,
                        created_at=get_current_timestamp(),
                        metadata={
                            "source_url": chunk.source_url,
                            "section": chunk.section,
                            "heading": chunk.heading,
                            "chunk_index": i,
                            "model": self.model,
                            "timestamp": get_current_timestamp().isoformat()
                        }
                    )

                    vectors.append(vector_repr)

                logger.info(f"Successfully generated embeddings for {len(vectors)} chunks")
                return vectors

            except cohere.CohereError as e:
                last_exception = e
                if "rate limit" in str(e).lower():
                    # Exponential backoff with jitter
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Rate limit hit on attempt {attempt + 1}, waiting {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    if attempt == max_retries:
                        logger.error(f"Failed to generate embeddings after {max_retries + 1} attempts: {str(e)}")
                        raise EmbeddingError(f"Error generating embeddings: {str(e)}")
                    else:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Embedding generation failed on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                        time.sleep(wait_time)
            except Exception as e:
                last_exception = e
                if attempt == max_retries:
                    logger.error(f"Unexpected error after {max_retries + 1} attempts: {str(e)}")
                    raise EmbeddingError(f"Unexpected error during embedding generation: {str(e)}")
                else:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Unexpected error on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)

        # If we get here, all retries have been exhausted
        raise EmbeddingError(f"Failed to generate embeddings after {max_retries + 1} attempts: {str(last_exception)}")

    def generate_single_embedding(self, text: str, chunk_id: str = None, max_retries: int = 3) -> VectorRepresentation:
        """
        Generate a single embedding for a text string with retry logic.

        Args:
            text: Text to generate embedding for
            chunk_id: Optional chunk ID to associate with the embedding
            max_retries: Maximum number of retry attempts

        Returns:
            VectorRepresentation object
        """
        if not text or len(text.strip()) == 0:
            raise EmbeddingError("Cannot generate embedding for empty text")

        # Try to generate embedding with retry logic
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                # Generate embedding using Cohere
                response = self.client.embed(
                    texts=[text],
                    model=self.model,
                    input_type="search_document"
                )

                embedding_vector = response.embeddings[0]

                vector_repr = VectorRepresentation(
                    id="",
                    vector=embedding_vector,
                    chunk_id=chunk_id or "",
                    model_used=self.model,
                    created_at=get_current_timestamp(),
                    metadata={
                        "model": self.model,
                        "timestamp": get_current_timestamp().isoformat()
                    }
                )

                logger.debug("Successfully generated single embedding")
                return vector_repr

            except cohere.CohereError as e:
                last_exception = e
                if "rate limit" in str(e).lower():
                    # Exponential backoff with jitter
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Rate limit hit on attempt {attempt + 1}, waiting {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    if attempt == max_retries:
                        logger.error(f"Failed to generate single embedding after {max_retries + 1} attempts: {str(e)}")
                        raise EmbeddingError(f"Error generating single embedding: {str(e)}")
                    else:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Single embedding generation failed on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                        time.sleep(wait_time)
            except Exception as e:
                last_exception = e
                if attempt == max_retries:
                    logger.error(f"Unexpected error after {max_retries + 1} attempts: {str(e)}")
                    raise EmbeddingError(f"Unexpected error during single embedding generation: {str(e)}")
                else:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Unexpected error on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)

        # If we get here, all retries have been exhausted
        raise EmbeddingError(f"Failed to generate single embedding after {max_retries + 1} attempts: {str(last_exception)}")

    def generate_embeddings_from_chunks(self, chunks: List[DocumentChunk]) -> List[VectorRepresentation]:
        """
        Generate embeddings specifically from DocumentChunk objects (integration with chunker).

        Args:
            chunks: List of DocumentChunk objects from the chunker

        Returns:
            List of VectorRepresentation objects
        """
        if not chunks:
            logger.warning("No chunks provided for embedding generation")
            return []

        logger.info(f"Generating embeddings from {len(chunks)} document chunks")
        return self.batch_generate_embeddings(chunks)

    def validate_embedding(self, vector_repr: VectorRepresentation) -> bool:
        """
        Validate an embedding vector.

        Args:
            vector_repr: VectorRepresentation to validate

        Returns:
            True if valid, False otherwise
        """
        if not vector_repr.vector or len(vector_repr.vector) == 0:
            logger.error("Vector representation has empty vector")
            return False

        # Check if vector dimensions are consistent (Cohere's model produces 1024-dim vectors)
        expected_dims = 1024
        if len(vector_repr.vector) != expected_dims:
            logger.warning(f"Vector has {len(vector_repr.vector)} dimensions, expected {expected_dims}")

        return True

    def batch_generate_embeddings(self, chunks: List[DocumentChunk], batch_size: int = 96) -> List[VectorRepresentation]:
        """
        Generate embeddings in batches to handle API limits and optimize performance.

        Args:
            chunks: List of DocumentChunk objects to generate embeddings for
            batch_size: Number of texts to process in each batch (Cohere max is 96)

        Returns:
            List of VectorRepresentation objects
        """
        if not chunks:
            return []

        all_vectors = []
        total_chunks = len(chunks)

        # Process in batches to handle API limits and optimize performance
        for i in range(0, total_chunks, batch_size):
            batch_chunks = chunks[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(total_chunks-1)//batch_size + 1} with {len(batch_chunks)} chunks")

            try:
                batch_vectors = self.generate_embeddings(batch_chunks)
                all_vectors.extend(batch_vectors)

                # Add a small delay between batches to avoid rate limiting
                time.sleep(config.RATE_LIMIT_DELAY)

            except Exception as e:
                logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                raise EmbeddingError(f"Error processing batch {i//batch_size + 1}: {str(e)}")

        logger.info(f"Successfully generated embeddings for {len(all_vectors)} chunks in {((total_chunks-1)//batch_size) + 1} batches")
        return all_vectors

    def optimize_performance(self, chunks: List[DocumentChunk], max_workers: int = 4) -> List[VectorRepresentation]:
        """
        Optimize performance using parallel processing for large volumes.

        Args:
            chunks: List of DocumentChunk objects to generate embeddings for
            max_workers: Maximum number of parallel workers

        Returns:
            List of VectorRepresentation objects
        """
        if not chunks:
            return []

        logger.info(f"Optimizing performance for {len(chunks)} chunks using parallel processing")

        # For now, using the batch approach which is already optimized
        # In a real implementation, we might use ThreadPoolExecutor for parallel API calls
        # but Cohere API rate limits would need to be carefully managed
        return self.batch_generate_embeddings(chunks)