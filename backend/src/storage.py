"""
Vector storage module for the RAG ingestion pipeline.
Handles storing vector representations in Qdrant database.
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict
import uuid
import time
import random
from .models.data_models import VectorRepresentation
from .config import config
from .errors import StorageError, ConfigurationError
from .logging_config import logger
from .utils import get_current_timestamp


class VectorStorage:
    """Handles storing and retrieving vector representations in Qdrant."""

    def __init__(self):
        """Initialize the vector storage with Qdrant client."""
        if not config.QDRANT_URL:
            raise ConfigurationError("QDRANT_URL environment variable is required")

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            prefer_grpc=False  # Using HTTP for better compatibility
        )

        self.collection_name = "document_embeddings"
        self.vector_size = config.get_vector_size()
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection exists with the correct schema."""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate configuration
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE  # Using cosine distance for embeddings
                    )
                )

                logger.info(f"Created new collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")

            # Create payload index for efficient metadata search
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="source_url",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

        except Exception as e:
            raise StorageError(f"Error setting up Qdrant collection: {str(e)}")

    def store_vectors(self, vectors: List[VectorRepresentation], max_retries: int = 3) -> bool:
        """
        Store a list of vector representations in Qdrant with retry logic.

        Args:
            vectors: List of VectorRepresentation objects to store
            max_retries: Maximum number of retry attempts

        Returns:
            True if successful, False otherwise
        """
        if not vectors:
            logger.warning("No vectors provided for storage")
            return True  # Not an error, just nothing to store

        logger.info(f"Storing {len(vectors)} vectors in Qdrant collection: {self.collection_name}")

        # Try to store vectors with retry logic
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                # Prepare points for insertion
                points = []
                for vector_repr in vectors:
                    point = models.PointStruct(
                        id=str(uuid.uuid4()),  # Generate a unique ID for the point
                        vector=vector_repr.vector,
                        payload={
                            "chunk_id": vector_repr.chunk_id,
                            "source_url": vector_repr.metadata.get("source_url", ""),
                            "section": vector_repr.metadata.get("section", ""),
                            "heading": vector_repr.metadata.get("heading", ""),
                            "model_used": vector_repr.model_used,
                            "created_at": vector_repr.created_at.isoformat() if vector_repr.created_at else "",
                            "chunk_index": vector_repr.metadata.get("chunk_index", 0),
                            "additional_metadata": vector_repr.metadata
                        }
                    )
                    points.append(point)

                # Upload points to Qdrant
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )

                logger.info(f"Successfully stored {len(vectors)} vectors in Qdrant")
                return True

            except Exception as e:
                last_exception = e
                if attempt == max_retries:
                    logger.error(f"Failed to store vectors after {max_retries + 1} attempts: {str(e)}")
                    raise StorageError(f"Error storing vectors in Qdrant: {str(e)}")
                else:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Vector storage failed on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)

        # If we get here, all retries have been exhausted
        raise StorageError(f"Failed to store vectors after {max_retries + 1} attempts: {str(last_exception)}")

    def store_single_vector(self, vector: VectorRepresentation, max_retries: int = 3) -> str:
        """
        Store a single vector representation in Qdrant with retry logic.

        Args:
            vector: VectorRepresentation object to store
            max_retries: Maximum number of retry attempts

        Returns:
            ID of the stored point
        """
        # Try to store vector with retry logic
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                point_id = str(uuid.uuid4())

                point = models.PointStruct(
                    id=point_id,
                    vector=vector.vector,
                    payload={
                        "chunk_id": vector.chunk_id,
                        "source_url": vector.metadata.get("source_url", ""),
                        "section": vector.metadata.get("section", ""),
                        "heading": vector.metadata.get("heading", ""),
                        "model_used": vector.model_used,
                        "created_at": vector.created_at.isoformat() if vector.created_at else "",
                        "chunk_index": vector.metadata.get("chunk_index", 0),
                        "additional_metadata": vector.metadata
                    }
                )

                # Upload single point to Qdrant
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=[point]
                )

                logger.debug(f"Successfully stored single vector with ID: {point_id}")
                return point_id

            except Exception as e:
                last_exception = e
                if attempt == max_retries:
                    logger.error(f"Failed to store single vector after {max_retries + 1} attempts: {str(e)}")
                    raise StorageError(f"Error storing single vector in Qdrant: {str(e)}")
                else:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Single vector storage failed on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {str(e)}")
                    time.sleep(wait_time)

        # If we get here, all retries have been exhausted
        raise StorageError(f"Failed to store single vector after {max_retries + 1} attempts: {str(last_exception)}")

    def search_vectors(self, query_vector: List[float], limit: int = 10,
                      filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar vectors in Qdrant.

        Args:
            query_vector: Vector to search for similar vectors
            limit: Maximum number of results to return
            filters: Optional filters for metadata search

        Returns:
            List of similar vectors with metadata
        """
        try:
            # Prepare filters if provided
            search_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        models.FieldCondition(
                            key=f"payload.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )

                if conditions:
                    search_filter = models.Filter(
                        must=conditions
                    )

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=limit
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "vector": result.vector,
                    "payload": result.payload,
                    "score": result.score
                })

            logger.debug(f"Search returned {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching vectors in Qdrant: {str(e)}")
            raise StorageError(f"Error searching vectors in Qdrant: {str(e)}")

    def verify_storage(self) -> bool:
        """
        Verify that vectors are stored and queryable.

        Returns:
            True if storage is working correctly, False otherwise
        """
        try:
            # Get the count of points in the collection
            count = self.client.count(
                collection_name=self.collection_name
            )

            logger.info(f"Verification: Collection contains {count.count} vectors")
            return True

        except Exception as e:
            logger.error(f"Error verifying storage: {str(e)}")
            return False

    def get_vector_by_id(self, point_id: str) -> Optional[Dict]:
        """
        Retrieve a vector by its ID.

        Args:
            point_id: ID of the vector to retrieve

        Returns:
            Vector data with metadata, or None if not found
        """
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[point_id]
            )

            if points and len(points) > 0:
                point = points[0]
                return {
                    "id": point.id,
                    "vector": point.vector,
                    "payload": point.payload
                }

            return None

        except Exception as e:
            logger.error(f"Error retrieving vector by ID {point_id}: {str(e)}")
            raise StorageError(f"Error retrieving vector by ID: {str(e)}")

    def validate_vector_storage(self, vector_repr: VectorRepresentation) -> bool:
        """
        Validate a vector representation before storage.

        Args:
            vector_repr: VectorRepresentation to validate

        Returns:
            True if valid, False otherwise
        """
        if not vector_repr.vector or len(vector_repr.vector) == 0:
            logger.error("Vector representation has empty vector")
            return False

        # Check if vector dimensions match expected size
        if len(vector_repr.vector) != self.vector_size:
            logger.warning(f"Vector has {len(vector_repr.vector)} dimensions, expected {self.vector_size}")
            return False

        # Check if required metadata exists
        if not vector_repr.chunk_id:
            logger.error("Vector representation missing required chunk_id")
            return False

        return True

    def store_embeddings(self, embeddings: List[VectorRepresentation]) -> bool:
        """
        Store embeddings specifically from the embedding generator output (integration with embeddings module).

        Args:
            embeddings: List of VectorRepresentation objects from the embeddings module

        Returns:
            True if successful, False otherwise
        """
        if not embeddings:
            logger.warning("No embeddings provided for storage")
            return True

        logger.info(f"Storing {len(embeddings)} embeddings from embedding generator")
        return self.store_vectors(embeddings)