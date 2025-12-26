"""
Integration tests for the complete RAG ingestion pipeline.
"""

import pytest
from unittest.mock import Mock, patch
from src.scraper import DocumentScraper
from src.chunker import TextChunker
from src.embeddings import EmbeddingGenerator
from src.storage import VectorStorage
from src.models.data_models import DocumentChunk, VectorRepresentation


class TestPipelineIntegration:
    """Test class for pipeline integration."""

    @patch('src.storage.QdrantClient')
    @patch('src.embeddings.cohere.Client')
    def test_complete_pipeline_flow(self, mock_cohere, mock_qdrant):
        """Test the complete pipeline flow from scraping to storage."""
        # Mock the clients
        mock_cohere_instance = Mock()
        mock_cohere.return_value = mock_cohere_instance
        mock_cohere_instance.embed.return_value = Mock()
        mock_cohere_instance.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

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
            # Initialize pipeline components
            scraper = DocumentScraper()
            chunker = TextChunker(chunk_size=50, overlap=5)
            embedding_generator = EmbeddingGenerator()
            vector_storage = VectorStorage()

            # Step 1: Simulate scraping (we'll create test chunks directly)
            test_content = "This is a sample document for testing the complete pipeline. " * 5
            initial_chunks = [
                DocumentChunk(
                    id="test-chunk-1",
                    content=test_content,
                    source_url="https://example.com/test",
                    section="Test Section",
                    heading="Test Heading",
                    metadata={"test": True}
                )
            ]

            # Step 2: Chunk the content
            all_chunks = []
            for chunk in initial_chunks:
                if len(chunk.content) > chunker.chunk_size:
                    sub_chunks = chunker.chunk_text(
                        text=chunk.content,
                        source_url=chunk.source_url,
                        section=chunk.section,
                        heading=chunk.heading,
                        metadata=chunk.metadata
                    )
                    all_chunks.extend(sub_chunks)
                else:
                    all_chunks.append(chunk)

            assert len(all_chunks) > 0
            for chunk in all_chunks:
                assert isinstance(chunk, DocumentChunk)
                assert len(chunk.content) > 0

            # Step 3: Generate embeddings
            embeddings = embedding_generator.generate_embeddings_from_chunks(all_chunks)
            assert len(embeddings) == len(all_chunks)
            for embedding in embeddings:
                assert isinstance(embedding, VectorRepresentation)
                assert len(embedding.vector) > 0
                assert embedding.chunk_id != ""

            # Step 4: Store embeddings
            success = vector_storage.store_embeddings(embeddings)
            assert success == True

            # Step 5: Verify storage
            storage_ok = vector_storage.verify_storage()
            assert storage_ok == True

        finally:
            # Restore original values
            config_module.config.COHERE_API_KEY = original_cohere_key
            config_module.config.QDRANT_URL = original_qdrant_url

    @patch('src.storage.QdrantClient')
    @patch('src.embeddings.cohere.Client')
    def test_pipeline_with_multiple_chunks(self, mock_cohere, mock_qdrant):
        """Test the pipeline with multiple document chunks."""
        # Mock the clients
        mock_cohere_instance = Mock()
        mock_cohere.return_value = mock_cohere_instance
        mock_cohere_instance.embed.return_value = Mock()
        # Return embeddings for multiple texts
        mock_cohere_instance.embed.return_value.embeddings = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ]

        mock_qdrant_instance = Mock()
        mock_qdrant.return_value = mock_qdrant_instance
        mock_qdrant_instance.get_collections.return_value = Mock()
        mock_qdrant_instance.get_collections.return_value.collections = []
        mock_qdrant_instance.upsert.return_value = None
        mock_qdrant_instance.count.return_value = Mock()
        mock_qdrant_instance.count.return_value.count = 3

        # Mock the configs
        import src.config as config_module
        original_cohere_key = config_module.config.COHERE_API_KEY
        original_qdrant_url = config_module.config.QDRANT_URL
        config_module.config.COHERE_API_KEY = "test-key"
        config_module.config.QDRANT_URL = "https://test-qdrant.com"

        try:
            # Initialize components
            chunker = TextChunker(chunk_size=30, overlap=3)
            embedding_generator = EmbeddingGenerator()
            vector_storage = VectorStorage()

            # Create multiple test chunks with different content
            test_chunks = [
                DocumentChunk(
                    id="chunk-1",
                    content="First document chunk with some content for testing purposes.",
                    source_url="https://example.com/doc1",
                    section="Document 1",
                    heading="Heading 1",
                    metadata={"doc_id": "1"}
                ),
                DocumentChunk(
                    id="chunk-2",
                    content="Second document chunk with different content for testing.",
                    source_url="https://example.com/doc2",
                    section="Document 2",
                    heading="Heading 2",
                    metadata={"doc_id": "2"}
                ),
                DocumentChunk(
                    id="chunk-3",
                    content="Third document chunk with more content for comprehensive testing.",
                    source_url="https://example.com/doc3",
                    section="Document 3",
                    heading="Heading 3",
                    metadata={"doc_id": "3"}
                )
            ]

            # Process each chunk through the pipeline
            all_embeddings = []
            for chunk in test_chunks:
                # Chunk if necessary
                if len(chunk.content) > chunker.chunk_size:
                    sub_chunks = chunker.chunk_text(
                        text=chunk.content,
                        source_url=chunk.source_url,
                        section=chunk.section,
                        heading=chunk.heading,
                        metadata=chunk.metadata
                    )
                else:
                    sub_chunks = [chunk]

                # Generate embeddings for the chunks
                embeddings = embedding_generator.generate_embeddings_from_chunks(sub_chunks)
                all_embeddings.extend(embeddings)

            # Verify we have embeddings
            assert len(all_embeddings) >= len(test_chunks)  # Could be more if chunks were split

            # Store all embeddings
            success = vector_storage.store_embeddings(all_embeddings)
            assert success == True

            # Verify storage
            storage_ok = vector_storage.verify_storage()
            assert storage_ok == True

        finally:
            # Restore original values
            config_module.config.COHERE_API_KEY = original_cohere_key
            config_module.config.QDRANT_URL = original_qdrant_url

    def test_error_handling_in_pipeline(self):
        """Test error handling throughout the pipeline."""
        from src.chunker import TextChunker
        from src.errors import ChunkingError

        # Test chunking error with empty content
        chunker = TextChunker()

        with pytest.raises(Exception):  # ChunkingError
            chunker.chunk_text(
                text="",
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading"
            )

        # Test chunking error with whitespace-only content
        with pytest.raises(Exception):  # ChunkingError
            chunker.chunk_text(
                text="   \n\t  \n   ",
                source_url="https://example.com",
                section="Test Section",
                heading="Test Heading"
            )