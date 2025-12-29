import requests
import json

# Test the chat endpoint
def test_chat():
    url = "http://localhost:8000/chat"

    # Test with the expected frontend format and various possible data structures
    test_cases = [
        # Expected frontend format
        {"query": "Explain the project"},

        # Other possible formats for compatibility
        {"message": "Hello, how are you?"},
        {"question": "What is artificial intelligence?"},
        {"prompt": "Explain robotics in simple terms"},
        {"text": "Tell me about machine learning"},
        {"input": "How does a chatbot work?"},
        {"user_message": "What can you help me with?"},

        # Complex objects
        {"message": "Hello, how are you?", "history": []},
        {"message": "What is ROS 2?", "userId": "123", "timestamp": "2023-01-01"}
    ]

    headers = {
        "Content-Type": "application/json"
    }

    for i, test_data in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Sending: {test_data}")

        try:
            response = requests.post(url, json=test_data, headers=headers)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                try:
                    response_json = response.json()
                    print(f"Response: {json.dumps(response_json, indent=2)}")
                    print("Success! The chat endpoint is working.")

                    # Check if response matches expected format for the main test case
                    if i == 0:  # First test case uses the expected format
                        if "answer" in response_json and "sources" in response_json:
                            print("✅ Response format matches frontend expectations!")
                        else:
                            print("⚠️ Response format may not match frontend expectations")
                except:
                    print(f"Could not parse JSON response: {response.text}")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_chat()