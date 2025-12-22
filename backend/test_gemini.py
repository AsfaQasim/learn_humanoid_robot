#!/usr/bin/env python3
"""
Test the Gemini API connection
"""
import os
import sys
import threading
import time
from dotenv import load_dotenv

load_dotenv()

def test_gemini_api():
    """Test the Gemini API connection"""
    print("Testing Gemini API connection...")

    result = {'success': False, 'error': None, 'completed': False}

    def run_test():
        try:
            import google.generativeai as genai

            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                print("ERROR: GEMINI_API_KEY not found in environment")
                result['error'] = "GEMINI_API_KEY not found"
                result['completed'] = True
                return

            print(f"Using Gemini API key: {gemini_api_key[:10]}...")

            genai.configure(api_key=gemini_api_key)
            print("SUCCESS: Gemini API configured")

            # Try to create a model instance
            model = genai.GenerativeModel('gemini-pro-latest')
            print("SUCCESS: Gemini model created")

            # Try a simple generation (this might take time)
            print("Testing simple generation...")
            response = model.generate_content(
                "Say hello in 10 words or less.",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=20,
                    temperature=0.1,
                )
            )

            if response and response.text:
                print(f"SUCCESS: Gemini response received: {response.text[:30]}...")
                result['success'] = True
            else:
                print("ERROR: Gemini returned empty response")
                result['error'] = "Empty response"

            result['completed'] = True
        except Exception as e:
            print(f"ERROR: Gemini API test failed: {e}")
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
        print("ERROR: Gemini API test timed out after 30 seconds")
        return False
    else:
        return result['success']

if __name__ == "__main__":
    print("Testing Gemini API functionality...")
    success = test_gemini_api()
    if success:
        print("\nGemini API test PASSED")
    else:
        print("\nGemini API test FAILED")
        print("The issue is likely with the Gemini API connection or configuration.")