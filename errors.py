"""
Custom error classes for the RAG retrieval pipeline.
"""

class RetrievalError(Exception):
    """Base exception class for retrieval operations."""
    pass


class ConfigurationError(RetrievalError):
    """Raised when there's an issue with configuration or environment variables."""
    pass


class ValidationError(RetrievalError):
    """Raised when there's an issue with data validation."""
    pass


class NetworkError(RetrievalError):
    """Raised when there are network-related issues."""
    pass


class RateLimitError(RetrievalError):
    """Raised when API rate limits are exceeded."""
    pass


class ProcessingError(RetrievalError):
    """Raised when there's a general processing error."""
    pass


class PipelineError(RetrievalError):
    """Raised when there's an issue with the retrieval pipeline."""
    pass


class CompatibilityError(RetrievalError):
    """Raised when there's an issue with embedding compatibility."""
    pass