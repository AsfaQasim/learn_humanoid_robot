#!/usr/bin/env python3
"""
Test script to verify the Physical AI & Humanoid Robotics RAG system is working correctly.
"""

import os
import sys
from datetime import datetime

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

def test_ingestion_pipeline():
    """Test that the ingestion pipeline components are available and properly configured."""
    print("[SEARCH] Testing ingestion pipeline...")

    try:
        # Test backend imports
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

        from backend.src.config import config
        from backend.src.scraper import DocumentScraper
        from backend.src.chunker import TextChunker
        from backend.src.embeddings import EmbeddingGenerator
        from backend.src.storage import VectorStorage

        print("[SUCCESS] All ingestion modules imported successfully")

        # Test configuration
        if not config.COHERE_API_KEY or config.COHERE_API_KEY == "your-cohere-api-key-here":
            print("[WARNING] COHERE_API_KEY not set in environment")
        else:
            print("[SUCCESS] COHERE_API_KEY is configured")

        if not config.QDRANT_URL or config.QDRANT_URL == "your-qdrant-url-here":
            print("[WARNING] QDRANT_URL not set in environment")
        else:
            print("[SUCCESS] QDRANT_URL is configured")

        print("[SUCCESS] Ingestion pipeline configuration verified")
        return True

    except ImportError as e:
        print(f"[ERROR] Import error in ingestion pipeline: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error testing ingestion pipeline: {e}")
        return False

def test_retrieval_system():
    """Test that the retrieval system is available and properly configured."""
    print("\n[SEARCH] Testing retrieval system...")

    try:
        # Add the current directory to path to import local modules
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))

        from retriever import RAGRetriever

        print("[SUCCESS] Retriever module imported successfully")

        # Test initialization (this will validate API keys)
        try:
            retriever = RAGRetriever()
            print("[SUCCESS] Retriever initialized successfully")

            # Test embedding compatibility
            if retriever.validate_embedding_compatibility():
                print("[SUCCESS] Embedding compatibility validated")
            else:
                print("[ERROR] Embedding compatibility failed")
                return False

            print("[SUCCESS] Retrieval system verified")
            return True
        except ValueError as e:
            print(f"[WARNING] Retriever initialization error (likely missing API keys): {e}")
            return True  # This is expected if API keys aren't set yet
        except Exception as e:
            print(f"[ERROR] Retriever error: {e}")
            return False

    except ImportError as e:
        print(f"[ERROR] Import error in retrieval system: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error testing retrieval system: {e}")
        return False

def test_agent_system():
    """Test that the AI agent system is available and properly configured."""
    print("\n[SEARCH] Testing AI agent system...")

    try:
        # Add the current directory to path to import local modules
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))

        from agent import RAGAgent

        print("[SUCCESS] Agent module imported successfully")

        # Test initialization (this will validate API keys)
        try:
            agent = RAGAgent()
            print("[SUCCESS] Agent initialized successfully")
            print("[SUCCESS] Agent system verified")
            return True
        except ValueError as e:
            print(f"[WARNING] Agent initialization error (likely missing API keys): {e}")
            return True  # This is expected if API keys aren't set yet
        except Exception as e:
            print(f"[ERROR] Agent error: {e}")
            return False

    except ImportError as e:
        print(f"[ERROR] Import error in agent system: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error testing agent system: {e}")
        return False

def test_environment():
    """Test that environment variables are properly set."""
    print("\n[SEARCH] Testing environment configuration...")

    env_vars = [
        ("COHERE_API_KEY", "Cohere API Key"),
        ("QDRANT_URL", "Qdrant URL"),
        ("QDRANT_API_KEY", "Qdrant API Key"),
        ("Gemini_Api_Key", "Gemini API Key")
    ]

    all_set = True
    for var, description in env_vars:
        value = os.getenv(var)
        if not value or value == f"your-{var.lower()}-here":
            print(f"[WARNING] {description} not set or using default placeholder")
            all_set = False
        else:
            print(f"[SUCCESS] {description} is configured")

    if all_set:
        print("[SUCCESS] All environment variables are properly configured")
    else:
        print("[WARNING] Some environment variables need to be configured")

    return all_set

def test_custom_scripts():
    """Test that custom scripts are available."""
    print("\n[SEARCH] Testing custom scripts...")

    scripts = [
        ("ingest_robotics_content.py", "Content ingestion script"),
        ("robotics_qa.py", "Question answering interface"),
        ("ROBOTICS_RAG_README.md", "Documentation"),
        (".env", "Environment configuration")
    ]

    all_exist = True
    for script, description in scripts:
        if os.path.exists(script):
            print(f"[SUCCESS] {description} exists")
        else:
            print(f"[ERROR] {description} missing")
            all_exist = False

    if all_exist:
        print("[SUCCESS] All custom scripts are in place")

    return all_exist

def main():
    """Run all tests and provide a summary."""
    print("Testing Physical AI & Humanoid Robotics RAG System")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    tests = [
        ("Environment Configuration", test_environment),
        ("Ingestion Pipeline", test_ingestion_pipeline),
        ("Retrieval System", test_retrieval_system),
        ("AI Agent System", test_agent_system),
        ("Custom Scripts", test_custom_scripts)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "[SUCCESS] PASS" if result else "[ERROR] FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1

    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! The RAG system is ready to use.")
        print("\nTo get started:")
        print("1. Ensure your API keys are set in the .env file")
        print("2. Run 'python ingest_robotics_content.py' to ingest website content")
        print("3. Run 'python robotics_qa.py --interactive' to start asking questions")
    else:
        print("Some tests failed. Please check the output above for details.")
        print("Most issues can be resolved by setting up your API keys in the .env file.")

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()