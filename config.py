"""
Configuration management for the RAG retrieval pipeline.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv
from typing import Optional, List


# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to manage application settings."""

    # Cohere Configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Processing Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    RATE_LIMIT_DELAY: float = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))

    # Validation
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration values are present."""
        required_vars = ["COHERE_API_KEY", "QDRANT_URL"]
        missing_vars = []

        for var_name in required_vars:
            value = getattr(cls, var_name)
            if not value or value == "":
                missing_vars.append(var_name)

        if missing_vars:
            print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
            return False

        return True

    @classmethod
    def validate_config_values(cls) -> List[str]:
        """
        Perform detailed validation of configuration values.

        Returns:
            List of validation error messages, empty if all valid
        """
        errors = []

        # Validate Cohere API key format (basic check)
        if cls.COHERE_API_KEY and len(cls.COHERE_API_KEY) < 10:
            errors.append("COHERE_API_KEY appears to be too short to be valid")

        # Validate Qdrant URL format
        if cls.QDRANT_URL:
            import re
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
                r'(?::[0-9]+)?'  # optional port
                r'(?:/.*)?$'  # optional path
            )
            if not url_pattern.match(cls.QDRANT_URL):
                errors.append(f"QDRANT_URL format appears invalid: {cls.QDRANT_URL}")

        # Validate chunk parameters
        if cls.CHUNK_SIZE <= 0:
            errors.append(f"CHUNK_SIZE must be positive, got: {cls.CHUNK_SIZE}")
        if cls.CHUNK_SIZE > 8192:  # Reasonable upper limit
            errors.append(f"CHUNK_SIZE seems too large: {cls.CHUNK_SIZE}")

        if cls.CHUNK_OVERLAP < 0:
            errors.append(f"CHUNK_OVERLAP cannot be negative, got: {cls.CHUNK_OVERLAP}")
        if cls.CHUNK_OVERLAP >= cls.CHUNK_SIZE:
            errors.append(f"CHUNK_OVERLAP ({cls.CHUNK_OVERLAP}) should be smaller than CHUNK_SIZE ({cls.CHUNK_SIZE})")

        if cls.RATE_LIMIT_DELAY < 0:
            errors.append(f"RATE_LIMIT_DELAY cannot be negative, got: {cls.RATE_LIMIT_DELAY}")

        return errors

    @classmethod
    def get_vector_size(cls) -> int:
        """Get the expected vector size for embeddings (default for Cohere embeddings)."""
        # Cohere's embed-english-v3.0 model produces 1024-dimensional vectors
        return 1024


# Global configuration instance
config = Config()