#!/usr/bin/env python3
"""
RAG-based Question Answering System for Physical AI & Humanoid Robotics

This script provides an interface to ask questions about the Physical AI & Humanoid Robotics content
that has been ingested into the vector database.
"""

import os
import sys
import argparse
from typing import Dict, Any

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from agent import RAGAgent
from retriever import RAGRetriever


def main():
    """Main function to run the Q&A system for Physical AI & Humanoid Robotics."""
    parser = argparse.ArgumentParser(description="RAG-based Q&A System for Physical AI & Humanoid Robotics")
    parser.add_argument("query", nargs="?", help="Question to ask about Physical AI & Humanoid Robotics")
    parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to retrieve (default: 5)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--validate", action="store_true", help="Validate the retrieval pipeline")
    parser.add_argument("--test-query", action="store_true", help="Run a test query to verify the system")

    args = parser.parse_args()

    print("[ROBOT] RAG-based Question Answering System for Physical AI & Humanoid Robotics")
    print("[BOOK] Content source: https://learn-humanoid-robot.vercel.app/")
    print("-" * 70)

    # Initialize the agent
    try:
        agent = RAGAgent()
        print("[SUCCESS] Agent initialized successfully")
    except ValueError as e:
        print(f"[ERROR] Error initializing agent: {e}")
        return

    # Validate embedding compatibility
    retriever = RAGRetriever()
    if not retriever.validate_embedding_compatibility():
        print("[ERROR] Embedding compatibility validation failed")
        return
    else:
        print("[SUCCESS] Embedding compatibility validated")

    # Run validation if requested
    if args.validate:
        print("\n[INFO] Validating retrieval pipeline...")
        test_queries = [
            "What is humanoid robotics?",
            "Explain physical AI concepts",
            "What are the applications of humanoid robots?",
            "How do robots interact with the physical world?"
        ]
        validation_results = retriever.validate_retrieval_pipeline(test_queries)
        print(f"\nValidation completed. Passed: {validation_results['validation_passed']}")
        if validation_results['validation_passed']:
            print("[SUCCESS] Retrieval pipeline is working correctly")
        else:
            print("[WARNING] There may be issues with the retrieval pipeline")

    # Test query if requested
    if args.test_query:
        print("\n[INFO] Running test query...")
        test_response = agent.query("What is Physical AI?", top_k=args.top_k)
        print(f"Test query response: {test_response['response'][:200]}...")
        print(f"Retrieved {test_response['retrieval_count']} chunks")

    # Interactive mode or single query
    if args.interactive or not args.query:
        # Interactive mode
        print("\n[INFO] Interactive mode - Ask questions about Physical AI & Humanoid Robotics")
        print("Examples of questions you can ask:")
        print("- What are the main components of a humanoid robot?")
        print("- Explain the principles of physical AI")
        print("- What are the applications of humanoid robots in real-world scenarios?")
        print("- How do humanoid robots perceive their environment?")
        print("\nType 'quit' to exit\n")

        while True:
            try:
                user_input = input("❓ Your question: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q', '']:
                    print("👋 Goodbye! Thanks for using the Physical AI & Humanoid Robotics Q&A system.")
                    break

                if not user_input:
                    continue

                print(f"\n🧠 Processing: '{user_input}'")
                response = agent.query(user_input, top_k=args.top_k)

                print(f"\n[ANSWER] Answer: {response['response']}")

                if response['retrieved_chunks']:
                    print(f"\n[INFO] Sources ({len(response['retrieved_chunks'])} document chunks used):")
                    for i, chunk in enumerate(response['retrieved_chunks'][:3]):  # Show first 3 chunks
                        source_url = chunk['source_url'] if chunk['source_url'] else "Unknown source"
                        print(f"  {i+1}. From: {source_url}")
                        print(f"     Content: {chunk['content'][:150]}{'...' if len(chunk['content']) > 150 else ''}")
                    if len(response['retrieved_chunks']) > 3:
                        print(f"  ... and {len(response['retrieved_chunks']) - 3} more chunks")
                else:
                    print("\n[WARNING] No relevant document chunks found for this query")

                print("\n" + "-" * 70 + "\n")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Physical AI & Humanoid Robotics Q&A system.")
                break
            except Exception as e:
                print(f"\n[ERROR] Error processing query: {e}")
                print("Please try again with a different question.\n")
    else:
        # Single query mode
        print(f"[INFO] Processing query: '{args.query}'")
        response = agent.query(args.query, top_k=args.top_k)

        print(f"\n[ANSWER] Answer: {response['response']}")

        if response['retrieved_chunks']:
            print(f"\n[INFO] Sources ({len(response['retrieved_chunks'])} document chunks used):")
            for i, chunk in enumerate(response['retrieved_chunks']):
                source_url = chunk['source_url'] if chunk['source_url'] else "Unknown source"
                print(f"  {i+1}. From: {source_url}")
                print(f"     Content: {chunk['content'][:200]}{'...' if len(chunk['content']) > 200 else ''}")
        else:
            print("\n[WARNING] No relevant document chunks found for this query")

    # Clean up
    agent.close()
    retriever.close()
    print("\n[SUCCESS] Session completed")


if __name__ == "__main__":
    main()