"""
Unit tests for the storage module.
"""

import pytest
from unittest.mock import Mock, patch
from src.storage import VectorStorage
from src.models.data_models import VectorRepresentation


class TestVectorStorage:
    """Test class for VectorStorage."""

    def test_vector_storage_initialization(self):
        """Test that vector storage initializes correctly."""
        # Mock the config to have QDRANT_URL
        import src.config as config_module
        original_url = config_module.config.QDRANT_URL
        config_module.config.QDRANT_URL = "https://test-qdrant.com"

        try:
            with patch('src.storage.QdrantClient') as mock_client:
                mock_client_instance = Mock()
                mock_client.return_value = mock_client_instance
                mock_client_instance.get_collections.return_value = Mock()
                mock_client_instance.get_collections.return_value.collections = []

                storage = VectorStorage()
                assert storage.collection_name == "document_embeddings"
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url

    def test_vector_storage_initialization_no_url(self):
        """Test that vector storage fails without QDRANT_URL."""
        import src.config as config_module
        original_url = config_module.config.QDRANT_URL
        config_module.config.QDRANT_URL = ""

        try:
            with pytest.raises(Exception):  # ConfigurationError
                VectorStorage()
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url

    def test_validate_vector_storage_valid(self):
        """Test vector storage validation with valid vector."""
        storage = VectorStorage.__new__(VectorStorage)  # Create without init
        storage.vector_size = 1024  # Set expected size directly

        vector_repr = VectorRepresentation(
            id="test-id",
            vector=[0.1] * 1024,  # 1024-dimensional vector
            chunk_id="chunk-123",
            model_used="test-model",
            created_at=None,
            metadata={}
        )

        result = storage.validate_vector_storage(vector_repr)
        assert result == True

    def test_validate_vector_storage_empty_vector(self):
        """Test vector storage validation with empty vector."""
        storage = VectorStorage.__new__(VectorStorage)  # Create without init
        storage.vector_size = 1024  # Set expected size directly

        vector_repr = VectorRepresentation(
            id="test-id",
            vector=[],
            chunk_id="chunk-123",
            model_used="test-model",
            created_at=None,
            metadata={}
        )

        result = storage.validate_vector_storage(vector_repr)
        assert result == False

    def test_validate_vector_storage_wrong_dimensions(self):
        """Test vector storage validation with wrong dimensions."""
        storage = VectorStorage.__new__(VectorStorage)  # Create without init
        storage.vector_size = 1024  # Set expected size directly

        vector_repr = VectorRepresentation(
            id="test-id",
            vector=[0.1] * 512,  # Wrong size - 512 instead of 1024
            chunk_id="chunk-123",
            model_used="test-model",
            created_at=None,
            metadata={}
        )

        result = storage.validate_vector_storage(vector_repr)
        assert result == False

    def test_validate_vector_storage_no_chunk_id(self):
        """Test vector storage validation with missing chunk_id."""
        storage = VectorStorage.__new__(VectorStorage)  # Create without init
        storage.vector_size = 1024  # Set expected size directly

        vector_repr = VectorRepresentation(
            id="test-id",
            vector=[0.1] * 1024,
            chunk_id="",  # Empty chunk_id
            model_used="test-model",
            created_at=None,
            metadata={}
        )

        result = storage.validate_vector_storage(vector_repr)
        assert result == False

    @patch('src.storage.QdrantClient')
    def test_store_single_vector_mock(self, mock_client):
        """Test storing a single vector with mocked Qdrant client."""
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

            # Create a test vector representation
            vector_repr = VectorRepresentation(
                id="test-id",
                vector=[0.1, 0.2, 0.3],
                chunk_id="chunk-123",
                model_used="test-model",
                created_at=None,
                metadata={
                    "source_url": "https://example.com",
                    "section": "Test Section",
                    "heading": "Test Heading"
                }
            )

            result_id = storage.store_single_vector(vector_repr)
            assert result_id is not None
            assert len(result_id) > 0
            mock_client_instance.upsert.assert_called_once()
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url

    @patch('src.storage.QdrantClient')
    def test_store_vectors_mock(self, mock_client):
        """Test storing multiple vectors with mocked Qdrant client."""
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

            # Create test vector representations
            vector_reprs = [
                VectorRepresentation(
                    id=f"test-id-{i}",
                    vector=[0.1, 0.2, 0.3],
                    chunk_id=f"chunk-{i}",
                    model_used="test-model",
                    created_at=None,
                    metadata={
                        "source_url": "https://example.com",
                        "section": "Test Section",
                        "heading": "Test Heading"
                    }
                )
                for i in range(2)
            ]

            result = storage.store_vectors(vector_reprs)
            assert result == True
            mock_client_instance.upsert.assert_called_once()
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url

    @patch('src.storage.QdrantClient')
    def test_verify_storage_mock(self, mock_client):
        """Test storage verification with mocked Qdrant client."""
        # Mock the Qdrant client
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.get_collections.return_value = Mock()
        mock_client_instance.get_collections.return_value.collections = []
        mock_client_instance.count.return_value = Mock()
        mock_client_instance.count.return_value.count = 5

        # Mock the config
        import src.config as config_module
        original_url = config_module.config.QDRANT_URL
        config_module.config.QDRANT_URL = "https://test-qdrant.com"

        try:
            storage = VectorStorage()
            result = storage.verify_storage()
            assert result == True
            mock_client_instance.count.assert_called_once()
        finally:
            # Restore original value
            config_module.config.QDRANT_URL = original_url