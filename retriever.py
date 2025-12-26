"""
Core retrieval logic and Qdrant integration for the RAG retrieval pipeline.
"""

import os
from typing import List, Dict, Optional, Tuple
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import cohere
from datetime import datetime
import time
import random
from config import config
from models import RetrievedChunk, QueryRequest
from errors import RetrievalError, ValidationError
from logging_config import logger
from utils import get_current_timestamp, generate_uuid


class RAGRetriever:
    """Handles semantic retrieval from Qdrant and pipeline validation."""

    def __init__(self):
        """Initialize the retriever with Cohere and Qdrant clients."""
        # Initialize Cohere client
        self.cohere_api_key = config.COHERE_API_KEY
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        self.cohere_client = cohere.Client(self.cohere_api_key)

        # Initialize Qdrant client
        self.qdrant_url = config.QDRANT_URL
        self.qdrant_api_key = config.QDRANT_API_KEY
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")

        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            prefer_grpc=False
        )

        # Use the same embedding model as used in ingestion
        self.embedding_model = "embed-english-v3.0"
        self.collection_name = "document_embeddings"

        print(f"Initialized RAG Retriever with collection: {self.collection_name}")

    def generate_query_embedding(self, query_text: str) -> List[float]:
        """
        Generate embedding for the query text using Cohere.

        Args:
            query_text: Text to generate embedding for

        Returns:
            List of floats representing the embedding vector
        """
        print(f"Generating embedding for query: '{query_text[:50]}{'...' if len(query_text) > 50 else ''}'")

        try:
            response = self.cohere_client.embed(
                texts=[query_text],
                model=self.embedding_model,
                input_type="search_query"  # Optimize for search queries
            )

            embedding = response.embeddings[0]
            print(f"Generated embedding with {len(embedding)} dimensions")
            return embedding
        except Exception as e:
            raise RetrievalError(f"Error generating embedding for query: {str(e)}")

    def retrieve_chunks(self, query_text: str, top_k: int = 5, score_threshold: float = 0.3) -> List[Dict]:
        """
        Retrieve top-k relevant chunks from Qdrant using cosine similarity.

        Args:
            query_text: Text to search for
            top_k: Number of top results to retrieve (default: 5)
            score_threshold: Minimum similarity score threshold (default: 0.3)

        Returns:
            List of retrieved chunks with metadata
        """
        print(f"Searching for: '{query_text}' (top-{top_k} results, score threshold: {score_threshold})")

        # Validate inputs
        if not query_text or len(query_text.strip()) == 0:
            raise ValidationError("Query text cannot be empty")

        if top_k <= 0:
            raise ValidationError(f"top_k must be positive, got: {top_k}")

        if not (0.0 <= score_threshold <= 1.0):
            raise ValidationError(f"score_threshold must be between 0.0 and 1.0, got: {score_threshold}")

        # Validate query complexity
        is_valid, issues = self.validate_query_complexity(query_text)
        if not is_valid:
            raise ValidationError(f"Query validation failed: {', '.join(issues)}")

        # Generate embedding for the query
        query_embedding = self.generate_query_embedding(query_text)

        # Search in Qdrant using cosine similarity
        try:
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True,
                with_vectors=False,
                score_threshold=score_threshold  # Minimum similarity threshold
            )

            # Format results
            results = []
            for idx, hit in enumerate(search_result):
                chunk_data = {
                    "rank": idx + 1,
                    "id": hit.id,
                    "content": hit.payload.get("content", "") if hit.payload else "",
                    "relevance_score": hit.score,
                    "source_url": hit.payload.get("source_url", "") if hit.payload else "",
                    "section": hit.payload.get("section", "") if hit.payload else "",
                    "heading": hit.payload.get("heading", "") if hit.payload else "",
                    "metadata": hit.payload or {},
                    "retrieved_at": datetime.now().isoformat()
                }
                results.append(chunk_data)

            # Handle case when query returns no relevant results
            if not results:
                print(f"[WARNING] No relevant chunks found for query: '{query_text[:50]}{'...' if len(query_text) > 50 else ''}' with threshold {score_threshold}")

            print(f"Retrieved {len(results)} relevant chunks")
            return results

        except Exception as e:
            logger.error(f"Error searching in Qdrant: {str(e)}")
            raise RetrievalError(f"Error searching in Qdrant: {str(e)}")

    def retrieve_chunks_with_retry(self, query_text: str, top_k: int = 5, score_threshold: float = 0.3,
                                   max_retries: int = 3, timeout: float = 30.0) -> List[Dict]:
        """
        Retrieve chunks with retry mechanism and timeout handling.

        Args:
            query_text: Text to search for
            top_k: Number of top results to retrieve
            score_threshold: Minimum similarity score threshold
            max_retries: Maximum number of retry attempts
            timeout: Timeout for each request in seconds

        Returns:
            List of retrieved chunks with metadata
        """
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                # Attempt to retrieve chunks
                results = self.retrieve_chunks(query_text, top_k, score_threshold)
                return results

            except Exception as e:
                last_exception = e
                if attempt == max_retries:
                    logger.error(f"Failed to retrieve chunks after {max_retries + 1} attempts: {str(e)}")
                    raise RetrievalError(f"Failed to retrieve chunks after retries: {str(e)}")
                else:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Chunk retrieval failed on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)

    def validate_query_complexity(self, query_text: str, max_length: int = 1000) -> Tuple[bool, List[str]]:
        """
        Add validation for complex or long queries.

        Args:
            query_text: Query text to validate
            max_length: Maximum allowed query length

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        if not query_text or len(query_text.strip()) == 0:
            issues.append("Query text is empty")
            return False, issues

        # Check length
        if len(query_text) > max_length:
            issues.append(f"Query length ({len(query_text)}) exceeds maximum allowed length ({max_length})")

        # Check for excessive special characters that might indicate a malformed query
        special_char_ratio = sum(1 for c in query_text if not c.isalnum() and not c.isspace()) / len(query_text)
        if special_char_ratio > 0.5:  # More than 50% special characters
            issues.append(f"Query has high ratio of special characters ({special_char_ratio:.2%})")

        # Check for SQL injection patterns (basic check)
        sql_patterns = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--', ';']
        for pattern in sql_patterns:
            if pattern.lower() in query_text.lower():
                issues.append(f"Potential SQL injection pattern detected: {pattern}")

        # Check for script tags (basic check)
        if '<script' in query_text or 'javascript:' in query_text:
            issues.append("Potential script injection detected")

        is_valid = len(issues) == 0
        if not is_valid:
            logger.warning(f"Query validation failed with issues: {', '.join(issues)}")

        return is_valid, issues

    def handle_connection_failures(self) -> bool:
        """
        Implement graceful handling of Qdrant connection failures.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            # Test connection by attempting a simple operation
            self.qdrant_client.get_collection(self.collection_name)
            logger.info("Qdrant connection is healthy")
            return True
        except Exception as e:
            logger.error(f"Qdrant connection failed: {str(e)}")

            # Try to reinitialize the client connection
            try:
                self.qdrant_client = QdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    prefer_grpc=False
                )
                # Test the reinitialized connection
                self.qdrant_client.get_collection(self.collection_name)
                logger.info("Qdrant connection re-established successfully")
                return True
            except Exception as reinit_error:
                logger.error(f"Failed to re-establish Qdrant connection: {str(reinit_error)}")
                return False

    def validate_embedding_compatibility(self) -> bool:
        """
        Validate that the embedding model used for retrieval matches the one used for ingestion.

        Returns:
            True if compatible, False otherwise
        """
        print("Validating embedding compatibility...")

        try:
            # Generate a test embedding
            test_embedding = self.generate_query_embedding("test query for validation")
            expected_dim = 1024  # Cohere's embed-english-v3.0 produces 1024-dim vectors

            if len(test_embedding) == expected_dim:
                print(f"[SUCCESS] Embedding compatibility validated: {len(test_embedding)} dimensions")
                return True
            else:
                print(f"[ERROR] Embedding dimension mismatch: expected {expected_dim}, got {len(test_embedding)}")
                return False
        except Exception as e:
            print(f"[ERROR] Error validating embedding compatibility: {str(e)}")
            return False

    def validate_retrieval_pipeline(self, test_queries: List[str]) -> Dict:
        """
        Validate the retrieval pipeline by testing multiple queries.

        Args:
            test_queries: List of test queries to validate against

        Returns:
            Validation results dictionary
        """
        print(f"Validating retrieval pipeline with {len(test_queries)} test queries...")

        validation_results = {
            "validation_passed": True,
            "test_queries_run": len(test_queries),
            "queries_results": [],
            "overall_accuracy": 0.0,
            "avg_relevance_score": 0.0,
            "total_retrieved_chunks": 0,
            "issues_found": []
        }

        total_relevance_score = 0.0
        total_chunks = 0

        for query in test_queries:
            print(f"\nTesting query: '{query}'")

            try:
                # Retrieve chunks for the query
                chunks = self.retrieve_chunks_with_retry(query, top_k=3)

                query_result = {
                    "query": query,
                    "retrieved_chunks": len(chunks),
                    "chunks": chunks,
                    "avg_relevance_score": 0.0,
                    "issues": []
                }

                if chunks:
                    avg_score = sum(c["relevance_score"] for c in chunks) / len(chunks)
                    query_result["avg_relevance_score"] = avg_score
                    total_relevance_score += avg_score
                    total_chunks += len(chunks)

                    # Check if relevance scores are acceptable
                    for chunk in chunks:
                        if chunk["relevance_score"] < 0.5:
                            query_result["issues"].append(
                                f"Low relevance score ({chunk['relevance_score']:.3f}) for chunk: {chunk['content'][:100]}..."
                            )
                else:
                    query_result["issues"].append("No chunks retrieved for this query")
                    validation_results["validation_passed"] = False

                validation_results["queries_results"].append(query_result)

            except Exception as e:
                error_msg = f"Error processing query '{query}': {str(e)}"
                validation_results["issues_found"].append(error_msg)
                validation_results["validation_passed"] = False
                print(f"Error: {error_msg}")

        # Calculate overall metrics
        if total_chunks > 0:
            validation_results["avg_relevance_score"] = total_relevance_score / len([qr for qr in validation_results["queries_results"] if qr["retrieved_chunks"] > 0])
            validation_results["total_retrieved_chunks"] = total_chunks
            # Simple accuracy calculation based on average relevance
            validation_results["overall_accuracy"] = min(1.0, validation_results["avg_relevance_score"] * 2)  # Scale to 0-1 range

        print(f"\nValidation Summary:")
        print(f"- Queries run: {validation_results['test_queries_run']}")
        print(f"- Total chunks retrieved: {validation_results['total_retrieved_chunks']}")
        print(f"- Average relevance score: {validation_results['avg_relevance_score']:.3f}")
        print(f"- Overall accuracy: {validation_results['overall_accuracy']:.3f}")
        print(f"- Passed: {validation_results['validation_passed']}")

        if validation_results["issues_found"]:
            print(f"- Issues found: {len(validation_results['issues_found'])}")

        return validation_results

    def close(self):
        """Close any resources if needed."""
        # Add cleanup logic if needed
        pass