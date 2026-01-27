import requests
import json

def test_backend_connection():
    """Test if the backend API is accessible"""
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Health check passed:", response.json())
        else:
            print("✗ Health check failed with status:", response.status_code)
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Is it running on http://localhost:8000?")
        return False
    
    # Test chat endpoint
    try:
        test_data = {
            "session_id": "test_session",
            "query_text": "Hello, are you working?",
            "collection_name": "document_embeddings"
        }
        
        response = requests.post(
            "http://localhost:8000/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Chat endpoint working. Response keys:", list(result.keys()))
        else:
            print("✗ Chat endpoint failed with status:", response.status_code)
            print("  Response:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to chat endpoint. Is the backend running?")
        return False
    except Exception as e:
        print("✗ Error testing chat endpoint:", str(e))
        return False
        
    return True

if __name__ == "__main__":
    print("Testing backend API connectivity...")
    print("="*50)
    success = test_backend_connection()
    if success:
        print("\n✓ All tests passed! Backend is accessible.")
    else:
        print("\n✗ Tests failed. Please check your backend setup.")