#!/usr/bin/env python3
"""
Script to verify that your robotics documentation was properly ingested into Qdrant.
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from src.config import DEFAULT_COLLECTION_NAME
from src.vector_store import get_qdrant_client


def verify_ingestion():
    """
    Verify that the robotics documentation was properly ingested into Qdrant.
    """
    print("Verifying robotics documentation ingestion...")

    # Get the Qdrant client
    qdrant_client = get_qdrant_client()

    try:
        # Check if collection exists
        collections = qdrant_client.get_collections().collections
        collection_names = [col.name for col in collections]

        if DEFAULT_COLLECTION_NAME not in collection_names:
            print(f"ERROR: Collection '{DEFAULT_COLLECTION_NAME}' not found!")
            return False

        # Get collection info
        collection_info = qdrant_client.get_collection(DEFAULT_COLLECTION_NAME)
        print(f"Collection '{DEFAULT_COLLECTION_NAME}' has {collection_info.points_count} points")

        if collection_info.points_count == 0:
            print("ERROR: Collection is empty!")
            return False

        # Show some sample content
        print(f"\nRetrieving sample content from the collection...")

        # Get sample points
        sample_points = qdrant_client.scroll(
            collection_name=DEFAULT_COLLECTION_NAME,
            limit=5
        )

        if sample_points[0]:
            print(f"\nSample of ingested content ({len(sample_points[0])} samples):")
            for i, point in enumerate(sample_points[0]):
                text_preview = point.payload["text"][:200] + "..." if len(point.payload["text"]) > 200 else point.payload["text"]
                print(f"\n{i+1}. File: {point.payload['file_name']}")
                print(f"   Relative Path: {point.payload['relative_path']}")
                print(f"   Chunk Index: {point.payload['chunk_index']}")
                print(f"   Content Preview: {text_preview}")
        else:
            print("No sample points retrieved!")
            return False

        # Test a search to make sure retrieval works
        print(f"\nTesting search functionality...")
        from src.services.rag_service import RAGService
        rag_service = RAGService(qdrant_client=qdrant_client)

        # Test with a robotics-related query
        test_docs = rag_service.retrieve(
            query="robotics fundamentals",
            collection_name=DEFAULT_COLLECTION_NAME,
            top_k=3
        )

        print(f"Retrieved {len(test_docs)} documents for 'robotics fundamentals' query")
        if test_docs:
            print("Sample retrieved content:")
            for i, doc in enumerate(test_docs[:2]):
                preview = doc[:150] + "..." if len(doc) > 150 else doc
                print(f"  {i+1}. {preview}")

        print(f"\nSUCCESS: Your robotics documentation has been properly ingested!")
        print(f"The chatbot will now use your real documentation content.")
        return True

    except Exception as e:
        print(f"ERROR: Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Verifying robotics documentation ingestion into Qdrant...")
    success = verify_ingestion()

    if success:
        print("\n[SUCCESS] Documentation ingestion completed successfully!")
        print("Your chatbot will now use your actual robotics content from the docs folder.")
    else:
        print("\n[FAILURE] Documentation ingestion verification failed!")
        sys.exit(1)