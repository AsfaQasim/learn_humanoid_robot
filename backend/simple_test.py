#!/usr/bin/env python3
"""
Simple test to verify the chatbot fix.
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


def simple_test():
    """Simple test without unicode characters"""
    print("Simple test of robotics query responses...")

    try:
        # Initialize RAG service
        qdrant_client = get_qdrant_client()
        rag_service = RAGService(qdrant_client=qdrant_client)

        # Test the original problematic query
        query = "Hey tell me about robotics or ROS from this book"
        print(f"Testing query: '{query}'")

        # Retrieve documents
        retrieved_docs = rag_service.retrieve(
            query=query,
            collection_name=DEFAULT_COLLECTION_NAME,
            top_k=5
        )

        print(f"Retrieved {len(retrieved_docs)} documents from the book")
        if retrieved_docs:
            print("Sample retrieved content:")
            for i, doc in enumerate(retrieved_docs[:2]):
                print(f"  Doc {i+1}: {doc[:100]}...")

        # Generate response
        response = rag_service.generate_response(
            query=query,
            retrieved_docs=retrieved_docs
        )

        print(f"\nGenerated response:")
        print(f"'{response}'")

        # Check if it's still returning the greeting
        greeting_check = "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant" in response
        content_check = len(response) > 150 and any(keyword in response.lower() for keyword in ['robot', 'ros', 'urdf', 'module', 'python'])

        print(f"\nResponse Analysis:")
        print(f"- Contains default greeting: {greeting_check}")
        print(f"- Contains content from book: {content_check}")

        if not greeting_check and content_check:
            print("SUCCESS: Chatbot is now properly answering with book content!")
        elif greeting_check:
            print("ISSUE: Still returning greeting instead of content")
        else:
            print("PARTIAL: Getting content but might need refinement")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Simple test of chatbot fix...")
    simple_test()