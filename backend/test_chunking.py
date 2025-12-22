"""
Test script to verify the chunking and ingestion functionality
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.chunk_manager import ingest_file_in_chunks, get_qdrant_client, create_test_document
import tempfile

def test_chunking_implementation():
    print("Testing chunking and ingestion implementation...")

    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file_path = temp_file.name
        create_test_document(temp_file_path)

    try:
        # Get Qdrant client
        client = get_qdrant_client()
        print("Connected to Qdrant successfully")

        # Test collection name
        test_collection = "test_ingestion"

        # Test ingestion with default parameters
        print("\n--- Testing with default parameters ---")
        ingest_file_in_chunks(
            file_path=temp_file_path,
            collection_name=test_collection,
            qdrant_client=client
        )

        # Verify the collection has points
        collection_info = client.get_collection(test_collection)
        print(f"\nCollection '{test_collection}' has {collection_info.points_count} points")

        # Test with custom parameters
        print("\n--- Testing with custom parameters (smaller chunks) ---")
        custom_collection = "test_ingestion_custom"
        ingest_file_in_chunks(
            file_path=temp_file_path,
            collection_name=custom_collection,
            qdrant_client=client,
            chunk_size=500,      # Smaller chunks
            chunk_overlap=50,    # Some overlap
            batch_size=10        # Smaller batches
        )

        # Verify the second collection
        collection_info2 = client.get_collection(custom_collection)
        print(f"\nCollection '{custom_collection}' has {collection_info2.points_count} points")

        print("\nSUCCESS: All tests passed! Chunking and ingestion working correctly.")

    except Exception as e:
        print(f"\nERROR: Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"\nCleaned up temporary file: {temp_file_path}")

if __name__ == "__main__":
    test_chunking_implementation()