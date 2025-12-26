"""
Demo script for the RAG Chatbot Agent with Qdrant retrieval integration.
This demonstrates the core functionality of the agent.
"""
import os
from agent import RAGAgent


def demo_basic_functionality():
    """Demonstrate the basic functionality of the RAG agent."""
    print("RAG Chatbot Agent Demo")
    print("=" * 50)

    # Check if required environment variables are set
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "COHERE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the full demo.")
        print("For now, we'll show the agent structure and capabilities...\n")
        return

    try:
        print("Initializing RAG Agent...")
        agent = RAGAgent()
        print("✅ Agent initialized successfully!\n")

        # Example queries to demonstrate functionality
        example_queries = [
            "What are the fundamental principles of robotics?",
            "Explain machine learning algorithms",
            "How does computer vision work?",
        ]

        print("Running example queries...\n")

        for i, query in enumerate(example_queries, 1):
            print(f"Query {i}: {query}")
            response = agent.query(query, top_k=3)

            print(f"Response: {response['response']}")
            print(f"Retrieved {response['retrieval_count']} chunks")
            if response['retrieved_chunks']:
                print(f"Sample chunk: {response['retrieved_chunks'][0]['content'][:100]}...")
            print("-" * 50)

        # Clean up
        agent.close()
        print("✅ Demo completed successfully!")

    except Exception as e:
        print(f"Error during demo: {e}")


def demo_error_handling():
    """Demonstrate the error handling capabilities."""
    print("\nError Handling Demo")
    print("=" * 50)

    # Test query validation
    agent = RAGAgent.__new__(RAGAgent)  # Create without calling __init__ to avoid API calls

    test_cases = [
        ("", "Empty query"),
        ("a" * 1001, "Overly long query"),
        ("SELECT * FROM users", "SQL injection attempt"),
        ("<script>alert('test')</script>", "Script injection attempt"),
    ]

    for query, description in test_cases:
        is_valid, issues = agent._validate_query_complexity(query)
        status = "Valid" if is_valid else "Invalid"
        print(f"{status} - {description}: {issues if issues else 'No issues'}")


if __name__ == "__main__":
    demo_basic_functionality()
    demo_error_handling()