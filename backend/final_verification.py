#!/usr/bin/env python3
"""
Final verification that the chatbot is working correctly with your robotics documentation.
"""
import os
import sys
import json
from pathlib import Path
import requests

# Add the backend directory to the path so we can import our modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from src.services.rag_service import RAGService
from src.vector_store import get_qdrant_client
from src.config import DEFAULT_COLLECTION_NAME


def test_direct_rag_service():
    """Test the RAG service directly"""
    print("=== DIRECT RAG SERVICE TEST ===")

    qdrant_client = get_qdrant_client()
    rag_service = RAGService(qdrant_client=qdrant_client)

    # Test various queries
    test_queries = [
        "tell me about robotics",
        "what is ROS 2",
        "explain URDF in robotics",
        "Hey tell me about robotics or ROS from this book",
        "how do Python agents connect to ROS controllers"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")

        # Retrieve docs
        docs = rag_service.retrieve(
            query=query,
            collection_name=DEFAULT_COLLECTION_NAME,
            top_k=3
        )

        print(f"  Retrieved {len(docs)} documents")

        # Generate response
        response = rag_service.generate_response(query=query, retrieved_docs=docs)

        print(f"  Response preview: {response[:100]}...")

        # Check if it's the problematic greeting
        is_greeting = "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant" in response
        has_content = len(response) > 100 and any(keyword in response.lower() for keyword in ['ros', 'robot', 'urdf', 'python', 'module'])

        print(f"  Is greeting (bad): {is_greeting}")
        print(f"  Has real content (good): {has_content}")


def test_api_endpoint():
    """Test the actual API endpoint"""
    print("\n=== API ENDPOINT TEST ===")

    # Assuming the backend is running on localhost:8000
    api_url = "http://localhost:8000/chat"

    test_payload = {
        "session_id": "test_session",
        "query_text": "Hey tell me about robotics or ROS from this book",
        "collection_name": DEFAULT_COLLECTION_NAME,
        "selected_text": None
    }

    try:
        response = requests.post(
            api_url,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"API Response: {result['response_text'][:200]}...")

            is_greeting = "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant" in result['response_text']
            has_sources = len(result.get('sources', [])) > 0

            print(f"Is greeting (bad): {is_greeting}")
            print(f"Has sources (good): {has_sources}")
            print(f"Number of sources: {len(result.get('sources', []))}")

        else:
            print(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        print("API endpoint not accessible. Make sure the backend server is running on port 8000.")
    except Exception as e:
        print(f"API Test Error: {e}")


if __name__ == "__main__":
    print("Final verification of chatbot fix...")

    print("\nThis test checks:")
    print("1. Direct RAG service functionality")
    print("2. API endpoint response")
    print("3. Whether greetings are properly handled")
    print("4. Whether real content is being returned")

    test_direct_rag_service()
    test_api_endpoint()

    print("\n" + "="*60)
    print("INTERPRETATION GUIDE:")
    print("✓ GOOD: Responses contain real content from your book")
    print("✗ BAD: Responses return the default greeting for content queries")
    print("ℹ️  If API test fails, restart your backend server to reload changes")
    print("="*60)