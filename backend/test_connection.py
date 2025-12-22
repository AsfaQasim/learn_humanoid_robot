#!/usr/bin/env python3
"""
Test script to check the connections to Qdrant and Gemini API
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_qdrant_connection():
    """Test Qdrant connection"""
    import threading
    import time

    result = {'success': False, 'error': None}

    def connect():
        try:
            from src.vector_store import get_qdrant_client
            print("Testing Qdrant connection...")
            client = get_qdrant_client()

            # Try to get collections
            collections = client.get_collections()
            print(f"SUCCESS: Qdrant connection successful. Found {len(collections.collections)} collections")

            # List collection names
            for collection in collections.collections:
                print(f"  - {collection.name}")

            result['success'] = True
        except Exception as e:
            result['error'] = e

    # Run the connection in a separate thread with timeout
    thread = threading.Thread(target=connect)
    thread.daemon = True
    thread.start()
    thread.join(timeout=10)  # Wait for 10 seconds

    if thread.is_alive():
        print("ERROR: Qdrant connection timed out after 10 seconds")
        return False
    elif result['error']:
        print(f"ERROR: Qdrant connection failed: {result['error']}")
        return False
    else:
        return result['success']

def test_gemini_connection():
    """Test Gemini API connection"""
    try:
        import google.generativeai as genai

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            print("✗ GEMINI_API_KEY not found in environment")
            return False

        print("Testing Gemini API configuration...")
        genai.configure(api_key=gemini_api_key)

        # Try to create a simple model instance
        model = genai.GenerativeModel('gemini-pro')
        print("SUCCESS: Gemini API configuration successful")

        return True
    except Exception as e:
        print(f"ERROR: Gemini API connection failed: {e}")
        return False

def test_embedding_model():
    """Test sentence transformer model"""
    try:
        print("Testing sentence transformer model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        test_text = "This is a test sentence."
        embedding = model.encode(test_text)
        print(f"SUCCESS: Sentence transformer model works. Embedding shape: {embedding.shape}")
        return True
    except Exception as e:
        print(f"ERROR: Sentence transformer model failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend connections...\n")

    qdrant_ok = test_qdrant_connection()
    print()

    gemini_ok = test_gemini_connection()
    print()

    embedding_ok = test_embedding_model()
    print()

    if qdrant_ok and gemini_ok and embedding_ok:
        print("SUCCESS: All connections are working properly!")
        sys.exit(0)
    else:
        print("ERROR: Some connections are not working properly.")
        sys.exit(1)