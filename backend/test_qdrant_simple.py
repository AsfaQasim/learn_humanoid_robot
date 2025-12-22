#!/usr/bin/env python3
"""
Simple test to verify the Qdrant connection issue
"""
import os
import sys
import threading
import time
from dotenv import load_dotenv

load_dotenv()

def test_qdrant_direct():
    """Test Qdrant connection directly"""
    print("Testing Qdrant connection directly...")

    result = {'success': False, 'error': None, 'completed': False}

    def connect():
        try:
            from qdrant_client import QdrantClient
            import os
            from dotenv import load_dotenv
            load_dotenv()

            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")

            print(f"Connecting to Qdrant at: {qdrant_url}")

            if qdrant_url and qdrant_api_key:
                client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key,
                )
            else:
                # Fallback to hardcoded values if environment variables are not set
                client = QdrantClient(
                    url="https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333",
                    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.cNySe9pbHewVBDaZXEUTGhpyWadhc3kWG5LWDTh51r0",
                )

            # Try to get collections with a simple request
            print("Attempting to get collections...")
            collections = client.get_collections()
            print(f"SUCCESS: Connected to Qdrant. Found {len(collections.collections)} collections")

            result['success'] = True
            result['completed'] = True
        except Exception as e:
            print(f"ERROR: Qdrant connection failed: {e}")
            result['error'] = e
            result['completed'] = True

    # Run with timeout
    thread = threading.Thread(target=connect)
    thread.daemon = True
    thread.start()
    thread.join(timeout=15)  # Wait for 15 seconds

    if not result['completed']:
        print("ERROR: Qdrant connection timed out after 15 seconds")
        return False
    else:
        return result['success']

if __name__ == "__main__":
    print("Testing Qdrant connection...")
    success = test_qdrant_direct()
    if success:
        print("Qdrant connection test PASSED")
    else:
        print("Qdrant connection test FAILED")
        print("\nThe issue is likely with the Qdrant connection.")
        print("This could be due to:")
        print("1. Network connectivity issues")
        print("2. Incorrect Qdrant URL or API key")
        print("3. Firewall blocking the connection")
        print("4. Qdrant cloud service being unavailable")