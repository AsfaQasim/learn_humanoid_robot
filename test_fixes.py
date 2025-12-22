#!/usr/bin/env python3
"""
Test script to verify the RAG service fixes work correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from src.services.rag_service import RAGService

def test_greeting_responses():
    """Test that the RAG service handles greetings properly"""
    print("Testing greeting responses...")

    # Create a mock RAG service instance (without actual Qdrant client for testing)
    class MockQdrantClient:
        pass

    rag_service = RAGService(qdrant_client=MockQdrantClient())

    # Mock the embedding model to avoid actual loading for this test
    class MockEmbeddingModel:
        def encode(self, text):
            return [0.1] * 384  # Mock embedding

    # Set the mock model directly
    rag_service._embedding_model = MockEmbeddingModel()

    # Test greetings
    greetings = ["hi", "hello", "hey", "Hi", "Hello there", "good morning"]

    for greeting in greetings:
        response = rag_service.generate_response(greeting, [])
        print(f"Input: '{greeting}' -> Response: '{response[:50]}...'")
        assert "Physical AI & Humanoid Robotics textbook assistant" in response, f"Failed for greeting: {greeting}"

    print("[PASS] Greeting responses work correctly!")

    # Test out-of-context questions
    print("\nTesting out-of-context responses...")
    out_of_context = ["What's the weather like?", "Tell me a joke", "What time is it?"]

    for query in out_of_context:
        response = rag_service.generate_response(query, [])
        print(f"Input: '{query}' -> Response: '{response[:50]}...'")
        assert "not part of the textbook context" in response or "Physical AI & Humanoid Robotics" in response, f"Failed for out-of-context: {query}"

    print("[PASS] Out-of-context responses work correctly!")

    # Test book-related questions with no context
    print("\nTesting book-related questions with no context...")
    book_questions = ["tell me about my book", "what is in the textbook", "describe the book"]

    for query in book_questions:
        response = rag_service.generate_response(query, [])
        print(f"Input: '{query}' -> Response: '{response[:50]}...'")
        assert "Physical AI & Humanoid Robotics textbook" in response, f"Failed for book question: {query}"

    print("[PASS] Book-related responses work correctly!")

    print("\n[SUCCESS] All tests passed! The fixes are working correctly.")

if __name__ == "__main__":
    test_greeting_responses()