#!/usr/bin/env python3
"""
Test to list available Gemini models
"""
import os
import sys
import threading
import time
from dotenv import load_dotenv

load_dotenv()

def list_gemini_models():
    """List available Gemini models"""
    print("Listing available Gemini models...")

    result = {'success': False, 'error': None, 'completed': False, 'models': []}

    def run_test():
        try:
            import google.generativeai as genai

            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                print("ERROR: GEMINI_API_KEY not found in environment")
                result['error'] = "GEMINI_API_KEY not found"
                result['completed'] = True
                return

            genai.configure(api_key=gemini_api_key)
            print("SUCCESS: Gemini API configured")

            # List available models
            print("Fetching available models...")
            models_gen = genai.list_models()
            models_list = list(models_gen)  # Convert generator to list
            print(f"Found {len(models_list)} models:")

            for model in models_list:
                print(f"  - {model.name}")
                if hasattr(model, 'supported_generation_methods') and 'generateContent' in model.supported_generation_methods:
                    print(f"    Supports generateContent: Yes")
                else:
                    print(f"    Supports generateContent: No")

            result['success'] = True
            result['completed'] = True
        except Exception as e:
            print(f"ERROR: Listing models failed: {e}")
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
        print("ERROR: Model listing timed out after 30 seconds")
        return [], False
    else:
        return result['models'], result['success']

if __name__ == "__main__":
    print("Listing available Gemini models...")
    models, success = list_gemini_models()
    if success:
        print("\nModel listing completed.")
    else:
        print("\nModel listing failed.")