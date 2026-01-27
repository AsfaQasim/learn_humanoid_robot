import requests
import json
import sys
import os

def test_backend_connectivity():
    """Comprehensive test for backend connectivity and functionality"""
    
    # Test configurations
    BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")
    
    print("="*60)
    print("COMPREHENSIVE BACKEND CONNECTIVITY TEST")
    print("="*60)
    print(f"Testing backend at: {BASE_URL}")
    print()
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✓ Health check passed: {health_data}")
        else:
            print(f"   ✗ Health check failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"   ✗ Cannot connect to backend. Is it running at {BASE_URL}?")
        print("   Make sure to start the backend with: cd backend && python run_server.py")
        return False
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
    
    print()
    
    # Test 2: Preflight OPTIONS request
    print("2. Testing preflight OPTIONS request...")
    try:
        response = requests.options(f"{BASE_URL}/chat", 
                                 headers={
                                     "Access-Control-Request-Method": "POST",
                                     "Access-Control-Request-Headers": "Content-Type",
                                     "Origin": "http://localhost:3000"
                                 })
        print(f"   ✓ OPTIONS request status: {response.status_code}")
        cors_headers = [header for header in response.headers if 'cors' in header.lower() or 'origin' in header.lower()]
        if cors_headers:
            print(f"   ✓ CORS headers present: {cors_headers}")
        else:
            print(f"   ⚠ No obvious CORS headers found, but this may be OK")
    except Exception as e:
        print(f"   ⚠ OPTIONS request failed (this might be OK): {e}")
    
    print()
    
    # Test 3: Chat endpoint
    print("3. Testing chat endpoint...")
    try:
        test_payload = {
            "session_id": "test_session_123",
            "query_text": "Hello, are you working?",
            "collection_name": "document_embeddings"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            headers={"Content-Type": "application/json"},
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Chat endpoint working")
            print(f"   Response keys: {list(result.keys())}")
            if 'answer' in result or 'response' in result:
                print(f"   ✓ Got expected response field")
            else:
                print(f"   ⚠ Response structure might differ from expected")
        elif response.status_code == 400:
            # This is often expected if no documents are indexed yet
            print(f"   ⚠ Chat endpoint returned 400 (expected if no documents indexed)")
            print(f"   Response: {response.text}")
        else:
            print(f"   ⚠ Chat endpoint returned unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.Timeout:
        print(f"   ✗ Chat endpoint request timed out (30 seconds)")
    except Exception as e:
        print(f"   ⚠ Chat endpoint error: {e}")
    
    print()
    
    # Test 4: CORS headers check
    print("4. Testing CORS headers...")
    try:
        # Make a request and check for CORS headers
        response = requests.get(f"{BASE_URL}/health")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print(f"   CORS Headers found:")
        for header, value in cors_headers.items():
            status = "✓" if value else "⚠"
            print(f"   {status} {header}: {value}")
    except Exception as e:
        print(f"   ⚠ Error checking CORS headers: {e}")
    
    print()
    
    # Test 5: Cross-origin simulation
    print("5. Simulating cross-origin request...")
    try:
        test_payload = {
            "session_id": "cross_origin_test",
            "query_text": "Cross-origin test",
            "collection_name": "document_embeddings"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:3000",  # Simulate cross-origin
                "Referer": "http://localhost:3000/"
            },
            json=test_payload
        )
        
        if response.status_code in [200, 400]:  # 400 is OK if no docs indexed
            print(f"   ✓ Cross-origin request handled successfully (status: {response.status_code})")
        else:
            print(f"   ⚠ Cross-origin request failed (status: {response.status_code})")
    except Exception as e:
        print(f"   ⚠ Cross-origin test error: {e}")
    
    print()
    print("="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("If you're still experiencing 'Failed to fetch' errors:")
    print("- Check that the backend is running on the correct port")
    print("- Verify your environment variables are set correctly")
    print("- Ensure no firewall is blocking the connection")
    print("- Check browser console for specific CORS errors")
    print("- Try clearing browser cache and cookies")
    
    return True

if __name__ == "__main__":
    test_backend_connectivity()