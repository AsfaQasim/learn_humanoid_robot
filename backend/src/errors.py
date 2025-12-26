"""
Custom error classes for the RAG ingestion pipeline.
"""

class PipelineError(Exception):
    """Base exception class for the ingestion pipeline."""
    pass


class ConfigurationError(PipelineError):
    """Raised when there's an issue with configuration or environment variables."""
    pass


class ScrapingError(PipelineError):
    """Raised when there's an issue with web scraping or content extraction."""
    pass


class ChunkingError(PipelineError):
    """Raised when there's an issue with text chunking."""
    pass


class EmbeddingError(PipelineError):
    """Raised when there's an issue with embedding generation."""
    pass


class StorageError(PipelineError):
    """Raised when there's an issue with vector storage."""
    pass


class ValidationError(PipelineError):
    """Raised when there's an issue with data validation."""
    pass


class RateLimitError(PipelineError):
    """Raised when API rate limits are exceeded."""
    pass


class NetworkError(PipelineError):
    """Raised when there are network-related issues."""
    pass


class ProcessingError(PipelineError):
    """Raised when there's a general processing error."""
    pass