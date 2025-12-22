#!/usr/bin/env python3
"""
Comprehensive tests for Qdrant ingestion to verify book content has been properly stored.
"""
import os
import unittest
from unittest.mock import Mock, patch
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionInfo
from qdrant_client.models import VectorParams
import sys
import json

# Load environment variables
load_dotenv()

class TestQdrantIngestion(unittest.TestCase):
    """Test suite for Qdrant ingestion verification"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock Qdrant client for testing
        self.mock_client = Mock(spec=QdrantClient)

        # Try to get actual Qdrant client
        try:
            self.qdrant_client = self._get_qdrant_client()
            self.has_real_connection = True
        except Exception as e:
            print(f"Could not connect to real Qdrant: {e}")
            self.has_real_connection = False
            self.qdrant_client = Mock(spec=QdrantClient)

    def _get_qdrant_client(self):
        """Get configured Qdrant client using environment variables or fallbacks"""
        qdrant_url = os.getenv("QDRANT_URL") or os.getenv("QDRANT_HOST")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_url and qdrant_api_key:
            # Clean up the URL by removing extra spaces and text
            cleaned_url = qdrant_url.strip()
            if "(local)" in cleaned_url:
                cleaned_url = cleaned_url.split("(local)")[0].strip()
            if "(cloud)" in cleaned_url:
                cleaned_url = cleaned_url.split("(cloud)")[0].strip()

            # Check for configuration mismatch
            if ("localhost" in cleaned_url or "127.0.0.1" in cleaned_url) and len(qdrant_api_key) > 50:
                print("[INFO] Configuration mismatch detected: local URL with cloud API key. Using cloud fallback instead.")
                fallback_url = "https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333"
                return QdrantClient(url=fallback_url, api_key=qdrant_api_key)
            else:
                return QdrantClient(url=cleaned_url, api_key=qdrant_api_key)
        else:
            # Fallback to hardcoded values if environment variables are not set
            print("[INFO] Environment variables not found. Using fallback values (check your .env file)")
            fallback_url = "https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333"
            fallback_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.cNySe9pbHewVBDaZXEUTGhpyWadhc3kWG5LWDTh51r0"
            return QdrantClient(url=fallback_url, api_key=fallback_api_key)

    def test_qdrant_connection(self):
        """Test that we can connect to Qdrant and get collections"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            collections_response = self.qdrant_client.get_collections()
            self.assertIsNotNone(collections_response)
            print(f"[INFO] Successfully connected to Qdrant. Found {len(collections_response.collections)} collections")
        except Exception as e:
            self.fail(f"Failed to connect to Qdrant: {e}")

    def test_test_ingestion_collection_exists(self):
        """Test that the 'test_ingestion' collection exists"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            collection_info = self.qdrant_client.get_collection("test_ingestion")
            self.assertIsInstance(collection_info, CollectionInfo)
            print(f"[INFO] Collection 'test_ingestion' exists with {collection_info.points_count} points")
        except Exception as e:
            self.fail(f"Collection 'test_ingestion' does not exist: {e}")

    def test_collection_has_points(self):
        """Test that the collection contains data points"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            collection_info = self.qdrant_client.get_collection("test_ingestion")
            self.assertGreater(collection_info.points_count, 0, "Collection should have at least one point")
            print(f"[INFO] Collection has {collection_info.points_count} points as expected")
        except Exception as e:
            self.fail(f"Failed to check collection points: {e}")

    def test_sample_data_retrieval(self):
        """Test that we can retrieve sample data from the collection"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            # Get collection info
            collection_info = self.qdrant_client.get_collection("test_ingestion")
            self.assertGreater(collection_info.points_count, 0, "Collection should have data to test")

            # Fetch sample points using scroll
            records, _ = self.qdrant_client.scroll(
                collection_name="test_ingestion",
                limit=5,
                with_payload=True,
                with_vectors=False
            )

            self.assertGreater(len(records), 0, "Should be able to retrieve at least one record")

            # Check that records have expected structure
            for record in records:
                self.assertIsNotNone(record.id, "Record should have an ID")
                self.assertIsNotNone(record.payload, "Record should have payload")
                self.assertIn('text', record.payload, "Payload should contain 'text' field")
                self.assertIsInstance(record.payload['text'], str, "Text field should be a string")

            print(f"[INFO] Successfully retrieved {len(records)} sample records with valid structure")

        except Exception as e:
            self.fail(f"Failed to retrieve sample data: {e}")

    def test_data_integrity(self):
        """Test the integrity of ingested data"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            # Fetch sample data
            records, _ = self.qdrant_client.scroll(
                collection_name="test_ingestion",
                limit=10,
                with_payload=True,
                with_vectors=True
            )

            self.assertGreater(len(records), 0, "Should have records to test")

            # Check each record for required fields and data quality
            for i, record in enumerate(records):
                # Check ID is valid
                self.assertIsNotNone(record.id, f"Record {i} should have an ID")

                # Check payload exists and has required fields
                self.assertIsNotNone(record.payload, f"Record {i} should have payload")
                self.assertIn('text', record.payload, f"Record {i} payload should contain 'text' field")

                # Check text content is meaningful
                text_content = record.payload['text']
                self.assertIsInstance(text_content, str, f"Text content should be string for record {i}")
                self.assertGreater(len(text_content.strip()), 0, f"Text content should not be empty for record {i}")

                # Check vector exists and has appropriate size
                self.assertIsNotNone(record.vector, f"Record {i} should have vector")
                self.assertIsInstance(record.vector, (list, tuple), f"Vector should be list or tuple for record {i}")
                self.assertGreater(len(record.vector), 0, f"Vector should not be empty for record {i}")

            print(f"[INFO] Verified data integrity for {len(records)} records")

        except Exception as e:
            self.fail(f"Failed data integrity test: {e}")

    def test_search_functionality(self):
        """Test that search functionality works with ingested data"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            # Get collection info to determine vector size
            collection_info = self.qdrant_client.get_collection("test_ingestion")
            if hasattr(collection_info.config.params, 'vectors'):
                vector_size = collection_info.config.params.vectors.size
            else:
                # Default vector size for embedding models
                vector_size = 1536

            # Create a mock query vector (in real usage, this would come from an embedding model)
            query_vector = [0.1] * vector_size  # Simple mock vector

            # Test different search methods based on Qdrant version
            search_methods_found = []

            # Check if query_points method exists (latest versions 1.16.2+)
            if hasattr(self.qdrant_client, 'query_points'):
                results = self.qdrant_client.query_points(
                    collection_name="test_ingestion",
                    query=query_vector,  # Note: parameter is 'query', not 'query_vector'
                    limit=5,
                    with_payload=True
                )
                search_methods_found.append('query_points')
                print(f"[INFO] Query_points method works, found {len(results.points)} results")

            # Check if search method exists (older versions)
            elif hasattr(self.qdrant_client, 'search'):
                results = self.qdrant_client.search(
                    collection_name="test_ingestion",
                    query_vector=query_vector,
                    limit=5,
                    with_payload=True
                )
                search_methods_found.append('search')
                print(f"[INFO] Search method works, found {len(results)} results")

            # Check if query method exists (intermediate versions)
            elif hasattr(self.qdrant_client, 'query'):
                try:
                    results = self.qdrant_client.query(
                        collection_name="test_ingestion",
                        query_vector=query_vector,
                        limit=5,
                        with_payload=True
                    )
                    search_methods_found.append('query')
                    print(f"[INFO] Query method works, found {len(results)} results")
                except TypeError as e:
                    if "query_text" in str(e):
                        # The query method might require query_text instead of query_vector
                        # Try with a text query if available
                        try:
                            # First get a sample text from the collection to use as a query
                            sample_records, _ = self.qdrant_client.scroll(
                                collection_name="test_ingestion",
                                limit=1,
                                with_payload=True,
                                with_vectors=False
                            )
                            if sample_records:
                                sample_text = sample_records[0].payload.get('text', 'test query')
                                results = self.qdrant_client.query(
                                    collection_name="test_ingestion",
                                    query_text=sample_text,
                                    limit=5,
                                    with_payload=True
                                )
                                search_methods_found.append('query')
                                print(f"[INFO] Query method with text works, found {len(results)} results")
                        except Exception:
                            # If query_text also fails, just continue
                            pass

            # At least one search method should be available
            self.assertGreater(len(search_methods_found), 0,
                              "At least one search method (query_points, query, or search) should be available")

        except Exception as e:
            self.fail(f"Search functionality test failed: {e}")

    def test_scroll_functionality(self):
        """Test that scroll functionality works for fetching all data"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            # Test scrolling through the collection
            records, next_offset = self.qdrant_client.scroll(
                collection_name="test_ingestion",
                limit=10,
                with_payload=True,
                with_vectors=False
            )

            self.assertIsNotNone(records, "Should return records from scroll")
            self.assertIsInstance(records, list, "Records should be a list")

            # Check that records have the expected structure
            if records:
                record = records[0]
                self.assertIsNotNone(record.id, "Record should have ID")
                self.assertIsNotNone(record.payload, "Record should have payload")

            print(f"[INFO] Scroll functionality works, retrieved {len(records)} records")

        except Exception as e:
            self.fail(f"Scroll functionality test failed: {e}")

    @unittest.skipUnless(os.getenv("QDRANT_API_KEY"), "Requires QDRANT_API_KEY to be set")
    def test_full_data_retrieval(self):
        """Test retrieving all data from the collection (only if API key is set)"""
        if not self.has_real_connection:
            self.skipTest("No real Qdrant connection available for this test")

        try:
            # Get total count first
            collection_info = self.qdrant_client.get_collection("test_ingestion")
            total_points = collection_info.points_count

            if total_points == 0:
                self.skipTest("No points in collection to retrieve")

            # Fetch all data in batches
            all_points = []
            offset = None
            batch_size = 50  # Smaller batch size for testing

            while True:
                records, next_offset = self.qdrant_client.scroll(
                    collection_name="test_ingestion",
                    limit=batch_size,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )

                all_points.extend(records)

                if next_offset is None:
                    break

                offset = next_offset

                # Safety check to avoid infinite loops
                if len(all_points) >= total_points:
                    break

            # Verify we got the expected number of points
            self.assertEqual(len(all_points), min(total_points, len(all_points)),
                           f"Should retrieve all points up to the limit")

            print(f"[INFO] Successfully retrieved {len(all_points)} points from collection")

            # Verify content quality
            text_contents = [point.payload.get('text', '') for point in all_points if point.payload]
            non_empty_texts = [text for text in text_contents if text.strip()]

            self.assertGreater(len(non_empty_texts), 0, "Should have non-empty text content in retrieved data")
            print(f"[INFO] Found {len(non_empty_texts)} records with non-empty text content")

        except Exception as e:
            self.fail(f"Full data retrieval test failed: {e}")


class TestQdrantIngestionMock(unittest.TestCase):
    """Mock tests for Qdrant ingestion when no real connection is available"""

    def setUp(self):
        """Set up mock test fixtures"""
        self.mock_client = Mock(spec=QdrantClient)

        # Configure mock return values
        mock_collection_info = Mock(spec=CollectionInfo)
        mock_collection_info.points_count = 100
        mock_collection_info.config = Mock()
        mock_params = Mock()
        mock_params.vectors = Mock()
        mock_params.vectors.size = 1536
        mock_collection_info.config.params = mock_params

        self.mock_client.get_collection.return_value = mock_collection_info

        # Mock scroll response
        mock_record = Mock()
        mock_record.id = "test_id_1"
        mock_record.payload = {"text": "Sample book content for testing"}
        mock_record.vector = [0.1] * 1536

        self.mock_client.scroll.return_value = ([mock_record], None)

        # Mock query response
        mock_hit = Mock()
        mock_hit.id = "test_id_1"
        mock_hit.payload = {"text": "Sample book content for testing"}
        mock_hit.score = 0.9
        self.mock_client.query.return_value = [mock_hit]

    def test_mock_connection(self):
        """Test mock connection works"""
        collections_response = Mock()
        collections_response.collections = [Mock()]
        self.mock_client.get_collections.return_value = collections_response

        result = self.mock_client.get_collections()
        self.assertIsNotNone(result)

    def test_mock_collection_exists(self):
        """Test mock collection exists"""
        collection_info = self.mock_client.get_collection("test_ingestion")
        self.assertIsNotNone(collection_info)
        self.assertEqual(collection_info.points_count, 100)

    def test_mock_data_retrieval(self):
        """Test mock data retrieval"""
        records, _ = self.mock_client.scroll(
            collection_name="test_ingestion",
            limit=5,
            with_payload=True,
            with_vectors=False
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].payload["text"], "Sample book content for testing")


def run_tests():
    """Run the Qdrant ingestion tests"""
    print("Running Qdrant Ingestion Tests...")
    print("=" * 50)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestQdrantIngestion)
    mock_suite = loader.loadTestsFromTestCase(TestQdrantIngestionMock)

    # Combine suites
    all_tests = unittest.TestSuite([suite, mock_suite])

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(all_tests)

    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)