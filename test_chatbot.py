"""
Quick test script to verify the chatbot endpoint is working correctly.
Run this after starting the backend server.
"""
import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_QUERY = "What is robotics?"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a sample query"""
    print(f"\nTesting /chat endpoint with query: '{TEST_QUERY}'")
    try:
        payload = {
            "query_text": TEST_QUERY,
            "collection_name": "document_embeddings"
        }

        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat endpoint working!")
            print(f"   Answer: {result.get('answer', 'N/A')[:200]}...")
            print(f"   Sources retrieved: {len(result.get('sources', []))}")
            return True
        else:
            print(f"❌ Chat endpoint returned error:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CHATBOT ENDPOINT TEST")
    print("=" * 60)
    print(f"Make sure your backend is running at {BASE_URL}\n")

    # Run tests
    health_ok = test_health_endpoint()
    chat_ok = test_chat_endpoint()

    print("\n" + "=" * 60)
    if health_ok and chat_ok:
        print("✅ ALL TESTS PASSED! Chatbot is working correctly.")
    else:
        print("❌ SOME TESTS FAILED. Check the errors above.")
    print("=" * 60)
