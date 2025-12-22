#!/usr/bin/env python3
"""
Test the full RAG service functionality
"""
import os
import sys
import threading
import time
from dotenv import load_dotenv

load_dotenv()

from src.config import DEFAULT_COLLECTION_NAME

def test_rag_service():
    """Test the full RAG service"""
    print("Testing RAG service...")

    result = {'success': False, 'error': None, 'completed': False}

    def run_test():
        try:
            from src.services.rag_service import RAGService
            from src.vector_store import get_qdrant_client
            import google.generativeai as genai

            # Test Qdrant connection first
            print("Testing Qdrant connection...")
            qdrant_client = get_qdrant_client()
            collections = qdrant_client.get_collections()
            print(f"SUCCESS: Qdrant connection works. Found {len(collections.collections)} collections")

            # Test RAG service initialization
            print("Initializing RAG service...")
            rag_service = RAGService(qdrant_client=qdrant_client)
            print("SUCCESS: RAG service initialized")

            # Test retrieval with a simple query
            print("Testing document retrieval...")
            retrieved_docs = rag_service.retrieve(
                query="test query",
                collection_name=DEFAULT_COLLECTION_NAME,  # Use configured default collection
                top_k=2
            )
            print(f"SUCCESS: Retrieved {len(retrieved_docs)} documents")

            # Test response generation (if Gemini is working)
            print("Testing response generation...")
            test_response = rag_service.generate_response(
                query="What is this document about?",
                retrieved_docs=["This is a test document for Qdrant ingestion."]
            )
            print(f"SUCCESS: Generated response: {test_response[:50]}...")

            result['success'] = True
            result['completed'] = True
        except Exception as e:
            print(f"ERROR: RAG service test failed: {e}")
            import traceback
            traceback.print_exc()
            result['error'] = e
            result['completed'] = True

    # Run with timeout
    thread = threading.Thread(target=run_test)
    thread.daemon = True
    thread.start()
    thread.join(timeout=30)  # Wait for 30 seconds

    if not result['completed']:
        print("ERROR: RAG service test timed out after 30 seconds")
        return False
    else:
        return result['success']

if __name__ == "__main__":
    print("Testing RAG service functionality...")
    success = test_rag_service()
    if success:
        print("\nRAG service test PASSED")
        print("The issue might be with the chat endpoint implementation itself.")
    else:
        print("\nRAG service test FAILED")
        print("The issue is likely in the RAG service or one of its dependencies.")