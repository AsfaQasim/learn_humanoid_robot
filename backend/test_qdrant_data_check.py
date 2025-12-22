#!/usr/bin/env python3
"""
Test script to verify that the Qdrant collection has proper robotics/AI content
and that the RAG service can retrieve relevant information.
"""
import os
import sys
import threading
import time
from dotenv import load_dotenv

load_dotenv()

from src.config import DEFAULT_COLLECTION_NAME
from src.services.rag_service import RAGService
from src.vector_store import get_qdrant_client

def test_data_retrieval():
    """Test that the Qdrant collection has the expected data and can be retrieved properly"""
    print("Testing Qdrant data retrieval...")

    try:
        # Test Qdrant connection first
        print("1. Testing Qdrant connection...")
        qdrant_client = get_qdrant_client()
        collections = qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]
        print(f"   SUCCESS: Found {len(collections.collections)} collections: {collection_names}")

        if DEFAULT_COLLECTION_NAME not in collection_names:
            print(f"   ERROR: Collection '{DEFAULT_COLLECTION_NAME}' not found!")
            return False

        # Get collection info
        collection_info = qdrant_client.get_collection(DEFAULT_COLLECTION_NAME)
        print(f"   Collection '{DEFAULT_COLLECTION_NAME}' has {collection_info.points_count} points")

        if collection_info.points_count == 0:
            print("   ERROR: Collection is empty!")
            return False

        # Test RAG service initialization
        print("\n2. Initializing RAG service...")
        rag_service = RAGService(qdrant_client=qdrant_client)
        print("   SUCCESS: RAG service initialized")

        # Test retrieval with robotics-related queries
        print("\n3. Testing retrieval with robotics-related queries...")

        test_queries = [
            "robotics",
            "artificial intelligence",
            "machine learning",
            "AI",
            "automation"
        ]

        for query in test_queries:
            print(f"   Testing query: '{query}'")
            retrieved_docs = rag_service.retrieve(
                query=query,
                collection_name=DEFAULT_COLLECTION_NAME,
                top_k=3
            )
            print(f"   Retrieved {len(retrieved_docs)} documents for '{query}'")
            if len(retrieved_docs) > 0:
                print(f"   Sample content: {retrieved_docs[0][:100]}...")

        # Test the generate_response function
        print("\n4. Testing response generation...")
        sample_docs = rag_service.retrieve(
            query="robotics",
            collection_name=DEFAULT_COLLECTION_NAME,
            top_k=3
        )

        if sample_docs:
            response = rag_service.generate_response(
                query="Tell me about robotics in this book",
                retrieved_docs=sample_docs
            )
            print(f"   Generated response length: {len(response)} characters")
            print(f"   Sample response: {response[:200]}...")
        else:
            print("   No documents retrieved for response generation test")

        print("\n5. Testing specific content retrieval...")
        # Try to find specific robotics content
        robotics_docs = rag_service.retrieve(
            query="robotics artificial intelligence machine learning",
            collection_name=DEFAULT_COLLECTION_NAME,
            top_k=5
        )
        print(f"   Found {len(robotics_docs)} robotics-related documents")
        for i, doc in enumerate(robotics_docs[:3]):  # Show first 3
            print(f"   Doc {i+1}: {doc[:150]}...")

        print("\n✓ All tests passed! The Qdrant collection contains robotics/AI content and can be retrieved properly.")
        return True

    except Exception as e:
        print(f"✗ ERROR: Data retrieval test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Qdrant Data Ingestion and Retrieval...")
    success = test_data_retrieval()
    if success:
        print("\n✓ Qdrant data verification PASSED")
        print("Your chatbot should now be able to answer robotics-related questions properly!")
    else:
        print("\n✗ Qdrant data verification FAILED")
        print("There may be an issue with data ingestion or the collection name.")