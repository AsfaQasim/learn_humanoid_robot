"""
Unit tests for the chunker module.
"""

import pytest
from src.chunker import TextChunker
from src.models.data_models import DocumentChunk


class TestTextChunker:
    """Test class for TextChunker."""

    def test_chunker_initialization(self):
        """Test that chunker initializes with correct defaults."""
        chunker = TextChunker()
        assert chunker.chunk_size > 0
        assert chunker.overlap >= 0

    def test_chunker_with_custom_sizes(self):
        """Test that chunker initializes with custom sizes."""
        chunker = TextChunker(chunk_size=256, overlap=25)
        assert chunker.chunk_size == 256
        assert chunker.overlap == 25

    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        chunker = TextChunker(chunk_size=50, overlap=5)
        text = "This is a sample text for chunking. " * 5  # Create a longer text
        chunks = chunker.chunk_text(
            text=text,
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading"
        )

        assert len(chunks) > 0
        for chunk in chunks:
            assert isinstance(chunk, DocumentChunk)
            assert len(chunk.content) > 0
            assert chunk.source_url == "https://example.com"
            assert chunk.section == "Test Section"
            assert chunk.heading == "Test Heading"

    def test_chunk_text_with_empty_input(self):
        """Test chunking with empty input."""
        chunker = TextChunker()

        with pytest.raises(Exception):  # ChunkingError
            chunker.chunk_text(
                text="",
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading"
            )

    def test_chunk_text_with_whitespace_only(self):
        """Test chunking with whitespace-only input."""
        chunker = TextChunker()

        with pytest.raises(Exception):  # ChunkingError
            chunker.chunk_text(
                text="   \n\t  \n   ",
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading"
            )

    def test_chunk_text_preserves_metadata(self):
        """Test that chunking preserves additional metadata."""
        chunker = TextChunker(chunk_size=100, overlap=10)
        text = "This is a sample text for testing metadata preservation. " * 3
        additional_metadata = {"custom_field": "custom_value", "test": True}

        chunks = chunker.chunk_text(
            text=text,
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading",
            metadata=additional_metadata
        )

        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata["custom_field"] == "custom_value"
            assert chunk.metadata["test"] == True
            assert chunk.metadata["source_url"] == "https://example.com"

    def test_validate_chunk_valid(self):
        """Test chunk validation with valid chunk."""
        chunker = TextChunker()
        chunk = DocumentChunk(
            id="test-id",
            content="This is valid content",
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading",
            metadata={}
        )

        assert chunker.validate_chunk(chunk) == True

    def test_validate_chunk_empty_content(self):
        """Test chunk validation with empty content."""
        chunker = TextChunker()
        chunk = DocumentChunk(
            id="test-id",
            content="",
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading",
            metadata={}
        )

        assert chunker.validate_chunk(chunk) == False

    def test_validate_chunk_whitespace_only(self):
        """Test chunk validation with whitespace-only content."""
        chunker = TextChunker()
        chunk = DocumentChunk(
            id="test-id",
            content="   \n\t  ",
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading",
            metadata={}
        )

        assert chunker.validate_chunk(chunk) == False

    def test_chunk_document_chunks(self):
        """Test chunking existing document chunks."""
        chunker = TextChunker(chunk_size=20, overlap=5)

        # Create a large document chunk
        large_content = "This is a large chunk of text that should be split into smaller pieces. " * 3
        original_chunk = DocumentChunk(
            id="original-id",
            content=large_content,
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading",
            metadata={"original": True}
        )

        # Re-chunk the document chunk
        new_chunks = chunker.chunk_document_chunks([original_chunk])

        assert len(new_chunks) > 1  # Should be split into multiple chunks
        for chunk in new_chunks:
            assert len(chunk.content) <= chunker.chunk_size * 2  # Allow some flexibility
            assert chunk.metadata["original"] == True  # Metadata should be preserved