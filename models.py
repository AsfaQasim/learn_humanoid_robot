"""
Data models for the RAG retrieval pipeline.
Defines Query Request, Retrieved Chunk, and Validation Result entities.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class QueryRequest:
    """Represents a text-based semantic search query with parameters."""

    query_text: str
    top_k: int = 5
    filters: Optional[Dict] = None
    metadata_fields: Optional[List[str]] = None

    def __post_init__(self):
        if not self.query_text or len(self.query_text.strip()) == 0:
            raise ValueError("Query text cannot be empty")

        if self.top_k <= 0 or self.top_k > 100:
            raise ValueError(f"top_k must be between 1 and 100, got: {self.top_k}")

        if self.filters is None:
            self.filters = {}

        if self.metadata_fields is None:
            self.metadata_fields = []


@dataclass
class RetrievedChunk:
    """Represents a document chunk returned by the semantic search with relevance score and metadata."""

    id: str
    content: str
    relevance_score: float
    source_url: str
    section: str
    heading: str
    chunk_metadata: Dict
    retrieved_at: datetime

    def __post_init__(self):
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Retrieved chunk content cannot be empty")

        if not (0.0 <= self.relevance_score <= 1.0):
            raise ValueError(f"Relevance score must be between 0.0 and 1.0, got: {self.relevance_score}")

        if not self.source_url:
            raise ValueError("Source URL is required for retrieved chunk")


@dataclass
class ValidationResult:
    """Represents the outcome of pipeline validation checks (compatibility, consistency, performance)."""

    id: str
    query_text: str
    retrieved_chunks_count: int
    avg_relevance_score: float
    validation_passed: bool
    issues_found: List[str]
    validation_timestamp: datetime
    validation_metrics: Dict

    def __post_init__(self):
        if self.retrieved_chunks_count < 0:
            raise ValueError(f"Retrieved chunks count cannot be negative, got: {self.retrieved_chunks_count}")

        if not (0.0 <= self.avg_relevance_score <= 1.0):
            raise ValueError(f"Average relevance score must be between 0.0 and 1.0, got: {self.avg_relevance_score}")

        if self.validation_metrics is None:
            self.validation_metrics = {}


@dataclass
class SearchParameters:
    """Represents search configuration parameters."""

    model_used: str
    similarity_threshold: float = 0.3
    max_distance: Optional[float] = None
    search_filters: Optional[Dict] = None
    query_embedding: Optional[List[float]] = None

    def __post_init__(self):
        if not self.model_used:
            raise ValueError("Model used is required for search parameters")

        if not (0.0 <= self.similarity_threshold <= 1.0):
            raise ValueError(f"Similarity threshold must be between 0.0 and 1.0, got: {self.similarity_threshold}")

        if self.search_filters is None:
            self.search_filters = {}