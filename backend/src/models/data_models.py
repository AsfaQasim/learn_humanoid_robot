"""
Data models for the RAG ingestion pipeline.
Defines Document Chunk, Metadata Record, and Vector Representation entities.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import uuid


@dataclass
class MetadataRecord:
    """Represents metadata for a processed document."""

    id: str
    source_url: str
    section_title: str
    heading_hierarchy: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    chunk_count: int = 0

    def __post_init__(self):
        if self.id is None or self.id == "":
            self.id = str(uuid.uuid4())


@dataclass
class DocumentChunk:
    """Represents a segment of text extracted from a URL with associated metadata."""

    id: str
    content: str
    source_url: str
    section: str
    heading: str
    metadata: Dict
    embedding: Optional[List[float]] = None

    def __post_init__(self):
        if self.id is None or self.id == "":
            self.id = str(uuid.uuid4())

        # Validate content is not empty
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Document chunk content cannot be empty")


@dataclass
class VectorRepresentation:
    """Represents a vector embedding of text content."""

    id: str
    vector: List[float]
    chunk_id: str
    model_used: str
    created_at: datetime
    metadata: Dict

    def __post_init__(self):
        if self.id is None or self.id == "":
            self.id = str(uuid.uuid4())

        # Validate vector dimensions
        if not self.vector or len(self.vector) == 0:
            raise ValueError("Vector representation cannot have empty vector")

        # Validate chunk_id reference
        if not self.chunk_id:
            raise ValueError("Vector representation must reference a chunk ID")