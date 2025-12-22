#!/usr/bin/env python3
"""
Test script to verify that the chatbot properly responds to robotics queries
using the ingested documentation content.
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from src.services.rag_service import RAGService
from src.vector_store import get_qdrant_client
from src.config import DEFAULT_COLLECTION_NAME


def test_robotics_responses():
    """
    Test that the chatbot properly responds to robotics queries with actual content.
    """
    print("Testing robotics query responses...")

    try:
        # Initialize RAG service
        qdrant_client = get_qdrant_client()
        rag_service = RAGService(qdrant_client=qdrant_client)

        # Test queries that should return robotics content
        test_queries = [
            "tell me about robotics from this book",
            "what is ROS 2",
            "explain URDF",
            "how do Python agents connect to ROS controllers",
            "Hey tell me about robotics or ROS from this book"  # This was your original query
        ]

        print(f"Testing with collection: {DEFAULT_COLLECTION_NAME}")

        for i, query in enumerate(test_queries):
            print(f"\n{i+1}. Testing query: '{query}'")

            # Retrieve documents
            retrieved_docs = rag_service.retrieve(
                query=query,
                collection_name=DEFAULT_COLLECTION_NAME,
                top_k=3
            )

            print(f"   Retrieved {len(retrieved_docs)} documents")

            if retrieved_docs:
                print(f"   Sample retrieved content: {retrieved_docs[0][:100]}...")

            # Generate response
            response = rag_service.generate_response(
                query=query,
                retrieved_docs=retrieved_docs
            )

            print(f"   Response length: {len(response)} characters")
            print(f"   Response preview: {response[:200]}...")

            # Check if it's the default greeting (which would indicate a problem)
            if "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant" in response and len(retrieved_docs) > 0:
                print(f"   ⚠️  WARNING: Returned greeting instead of content despite having documents!")
            else:
                print(f"   ✅ Response appears to use content properly")

        # Test a specific scenario that was problematic
        print(f"\n{'='*60}")
        print("DETAILED TEST: Original problematic query")
        print(f"{'='*60}")

        problematic_query = "Hey tell me about robotics or ROS from this book"
        docs = rag_service.retrieve(
            query=problematic_query,
            collection_name=DEFAULT_COLLECTION_NAME,
            top_k=5
        )

        print(f"Query: '{problematic_query}'")
        print(f"Retrieved {len(docs)} documents:")
        for j, doc in enumerate(docs):
            print(f"  Doc {j+1}: {doc[:80]}...")

        response = rag_service.generate_response(
            query=problematic_query,
            retrieved_docs=docs
        )

        print(f"\nGenerated response:")
        print(f"'{response}'")

        if "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant" in response:
            print(f"\n❌ ISSUE CONFIRMED: Still returning greeting instead of content")
        else:
            print(f"\n✅ FIXED: Now properly responding with content!")

        return True

    except Exception as e:
        print(f"ERROR: Testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Testing robotics query responses...")
    success = test_robotics_responses()

    if success:
        print("\n✅ Response testing completed!")
    else:
        print("\n❌ Response testing failed!")
        sys.exit(1)