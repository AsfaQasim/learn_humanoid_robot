"""
Performance and edge case tests for the RAG ingestion pipeline.
"""

import pytest
import time
from unittest.mock import Mock, patch
from src.chunker import TextChunker
from src.embeddings import EmbeddingGenerator
from src.storage import VectorStorage
from src.models.data_models import DocumentChunk, VectorRepresentation


class TestPerformanceAndEdgeCases:
    """Test class for performance and edge cases."""

    def test_chunker_performance_large_text(self):
        """Test chunker performance with large text."""
        chunker = TextChunker(chunk_size=512, overlap=50)

        # Create a large text (simulating a large document)
        large_text = "This is a sentence. " * 1000  # 1000 sentences
        start_time = time.time()

        chunks = chunker.chunk_text(
            text=large_text,
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading"
        )

        end_time = time.time()
        processing_time = end_time - start_time

        # Ensure processing is reasonably fast (less than 10 seconds for this test)
        assert processing_time < 10.0
        assert len(chunks) > 0

    def test_chunker_with_very_small_chunk_size(self):
        """Test chunker behavior with very small chunk size."""
        chunker = TextChunker(chunk_size=5, overlap=2)

        text = "This is a test sentence for very small chunks."
        chunks = chunker.chunk_text(
            text=text,
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading"
        )

        # Should create multiple small chunks
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk.content) > 0

    def test_chunker_with_large_overlap(self):
        """Test chunker behavior with large overlap relative to chunk size."""
        chunker = TextChunker(chunk_size=50, overlap=45)  # Large overlap

        text = "This is a test sentence. " * 20  # Create longer text
        chunks = chunker.chunk_text(
            text=text,
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading"
        )

        assert len(chunks) > 1
        # With large overlap, consecutive chunks should have significant overlap

    def test_embedding_generator_with_empty_list(self):
        """Test embedding generator with empty list."""
        # Mock the config to have an API key
        import src.config as config_module
        original_api_key = config_module.config.COHERE_API_KEY
        config_module.config.COHERE_API_KEY = "test-key"

        try:
            with patch('src.embeddings.cohere.Client'):
                generator = EmbeddingGenerator()
                result = generator.generate_embeddings([])
                assert result == []
        finally:
            # Restore original value
            config_module.config.COHERE_API_KEY = original_api_key

    def test_embedding_generator_with_single_large_text(self):
        """Test embedding generator with a single large text chunk."""
        # Mock the config to have an API key
        import src.config as config_module
        original_api_key = config_module.config.COHERE_API_KEY
        config_module.config.COHERE_API_KEY = "test-key"

        try:
            with patch('src.embeddings.cohere.Client') as mock_client:
                mock_cohere_instance = Mock()
                mock_client.return_value = mock_cohere_instance
                mock_cohere_instance.embed.return_value = Mock()
                mock_cohere_instance.embed.return_value.embeddings = [[0.1] * 1024]

                generator = EmbeddingGenerator()

                # Create a large chunk
                large_chunk = DocumentChunk(
                    id="large-chunk",
                    content="This is a test sentence. " * 100,  # Large content
                    source_url="https://example.com",
                    section="Test Section",
                    heading="Test Heading",
                    metadata={}
                )

                result = generator.generate_embeddings([large_chunk])
                assert len(result) == 1
                assert isinstance(result[0], VectorRepresentation)
        finally:
            # Restore original value
            config_module.config.COHERE_API_KEY = original_api_key

    @patch('src.storage.QdrantClient')
    def test_storage_with_empty_list(self, mock_client):
        """Test storage with empty list of vectors."""
        # Mock the Qdrant client
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.get_collections.return_value = Mock()
        mock_client_instance.get_collections.return_value.collections = []
        mock_client_instance.upsert.return_value = None

        # Mock the config
        import src.config as config_module
        original_url = config_module.config.QDRANT_URL
        config_module.config.QDRANT_URL = "https://test-qdrant.com"

        try:
            storage = VectorStorage()
            result = storage.store_vectors([])
            assert result == True  # Should return True for empty list
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url

    @patch('src.storage.QdrantClient')
    def test_storage_single_vector(self, mock_client):
        """Test storing a single vector."""
        # Mock the Qdrant client
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.get_collections.return_value = Mock()
        mock_client_instance.get_collections.return_value.collections = []
        mock_client_instance.upsert.return_value = None

        # Mock the config
        import src.config as config_module
        original_url = config_module.config.QDRANT_URL
        config_module.config.QDRANT_URL = "https://test-qdrant.com"

        try:
            storage = VectorStorage()

            vector_repr = VectorRepresentation(
                id="test-id",
                vector=[0.1] * 1024,
                chunk_id="chunk-123",
                model_used="test-model",
                created_at=None,
                metadata={}
            )

            result_id = storage.store_single_vector(vector_repr)
            assert result_id is not None
            assert len(result_id) > 0
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url

    def test_document_chunk_validation(self):
        """Test DocumentChunk validation."""
        # Test with valid content
        valid_chunk = DocumentChunk(
            id="valid-id",
            content="This is valid content",
            source_url="https://example.com",
            section="Test Section",
            heading="Test Heading",
            metadata={}
        )
        assert len(valid_chunk.content.strip()) > 0

        # Test with empty content - should raise error during initialization
        with pytest.raises(ValueError):
            DocumentChunk(
                id="empty-id",
                content="",  # Empty content
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading",
                metadata={}
            )

        # Test with whitespace-only content - should raise error during initialization
        with pytest.raises(ValueError):
            DocumentChunk(
                id="whitespace-id",
                content="   \n\t  \n   ",  # Whitespace only
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading",
                metadata={}
            )

    def test_vector_representation_validation(self):
        """Test VectorRepresentation validation."""
        # Test with valid vector
        valid_vector = VectorRepresentation(
            id="valid-id",
            vector=[0.1, 0.2, 0.3],
            chunk_id="chunk-123",
            model_used="test-model",
            created_at=None,
            metadata={}
        )
        assert len(valid_vector.vector) > 0
        assert valid_vector.chunk_id != ""

        # Test with empty vector - should raise error during validation
        with pytest.raises(ValueError):
            VectorRepresentation(
                id="empty-vec-id",
                vector=[],  # Empty vector
                chunk_id="chunk-123",
                model_used="test-model",
                created_at=None,
                metadata={}
            )

        # Test with no chunk_id - should raise error during validation
        with pytest.raises(ValueError):
            VectorRepresentation(
                id="no-chunk-id",
                vector=[0.1, 0.2, 0.3],
                chunk_id="",  # Empty chunk_id
                model_used="test-model",
                created_at=None,
                metadata={}
            )

    @patch('src.storage.QdrantClient')
    @patch('src.embeddings.cohere.Client')
    def test_pipeline_with_edge_case_inputs(self, mock_cohere, mock_qdrant):
        """Test the pipeline with edge case inputs."""
        # Mock the clients
        mock_cohere_instance = Mock()
        mock_cohere.return_value = mock_cohere_instance
        mock_cohere_instance.embed.return_value = Mock()
        mock_cohere_instance.embed.return_value.embeddings = [[0.1] * 1024]

        mock_qdrant_instance = Mock()
        mock_qdrant.return_value = mock_qdrant_instance
        mock_qdrant_instance.get_collections.return_value = Mock()
        mock_qdrant_instance.get_collections.return_value.collections = []
        mock_qdrant_instance.upsert.return_value = None
        mock_qdrant_instance.count.return_value = Mock()
        mock_qdrant_instance.count.return_value.count = 1

        # Mock the configs
        import src.config as config_module
        original_cohere_key = config_module.config.COHERE_API_KEY
        original_qdrant_url = config_module.config.QDRANT_URL
        config_module.config.COHERE_API_KEY = "test-key"
        config_module.config.QDRANT_URL = "https://test-qdrant.com"

        try:
            from src.chunker import TextChunker
            from src.embeddings import EmbeddingGenerator
            from src.storage import VectorStorage

            chunker = TextChunker(chunk_size=20, overlap=5)
            embedding_generator = EmbeddingGenerator()
            vector_storage = VectorStorage()

            # Test with minimal content
            minimal_chunk = DocumentChunk(
                id="minimal",
                content="A short text.",
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading",
                metadata={}
            )

            # Chunk the minimal content
            if len(minimal_chunk.content) > chunker.chunk_size:
                chunks = chunker.chunk_text(
                    text=minimal_chunk.content,
                    source_url=minimal_chunk.source_url,
                    section=minimal_chunk.section,
                    heading=minimal_chunk.heading,
                    metadata=minimal_chunk.metadata
                )
            else:
                chunks = [minimal_chunk]

            # Generate embeddings
            embeddings = embedding_generator.generate_embeddings_from_chunks(chunks)

            # Store embeddings
            success = vector_storage.store_embeddings(embeddings)
            assert success == True

            # Verify storage
            storage_ok = vector_storage.verify_storage()
            assert storage_ok == True

        finally:
            # Restore original values
            config_module.config.COHERE_API_KEY = original_cohere_key
            config_module.config.QDRANT_URL = original_qdrant_url