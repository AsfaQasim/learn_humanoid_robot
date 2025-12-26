"""
Utility functions for the RAG ingestion pipeline.
"""

import uuid
from datetime import datetime
from typing import Optional


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get the current timestamp."""
    return datetime.now()


def get_timestamp_from_string(timestamp_str: str) -> Optional[datetime]:
    """Convert a timestamp string to a datetime object."""
    try:
        # Try ISO format first
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except ValueError:
        try:
            # Try common format
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None


def validate_url(url: str) -> bool:
    """Basic URL validation."""
    if not url:
        return False

    url = url.strip().lower()
    return url.startswith(('http://', 'https://'))


def sanitize_text(text: str) -> str:
    """Sanitize text by removing extra whitespace."""
    if not text:
        return ""

    # Normalize whitespace
    text = ' '.join(text.split())
    return text.strip()


def chunk_list(lst: list, chunk_size: int) -> list:
    """Split a list into chunks of specified size."""
    if not lst:
        return []

    chunks = []
    for i in range(0, len(lst), chunk_size):
        chunks.append(lst[i:i + chunk_size])

    return chunks