#!/usr/bin/env python3
"""
RAG Data Retrieval and Pipeline Validation Script

This script performs semantic search against stored embeddings in Qdrant,
retrieves top-k relevant chunks with metadata using cosine similarity,
and validates the retrieval pipeline.
"""

import os
import argparse
import sys
from typing import List, Dict, Optional
from datetime import datetime
from config import Config, config
from retriever import RAGRetriever
from models import QueryRequest, RetrievedChunk, ValidationResult
from errors import ConfigurationError, RetrievalError


def main():
    """Main function to run the retrieval system."""
    parser = argparse.ArgumentParser(description="RAG Data Retrieval and Pipeline Validation")
    parser.add_argument("query", nargs="?", help="Query text for semantic search")
    parser.add_argument("--top-k", type=int, default=5, help="Number of top results to retrieve (default: 5)")
    parser.add_argument("--validate", action="store_true", help="Run pipeline validation")
    parser.add_argument("--test-queries", nargs="+", help="Test queries for validation")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

    try:
        # Validate configuration
        if not Config.validate():
            print("ERROR: Configuration validation failed")
            sys.exit(1)

        # Validate configuration values in detail
        config_errors = Config.validate_config_values()
        if config_errors:
            print("ERROR: Configuration validation errors found:")
            for error in config_errors:
                print(f"  - {error}")
            sys.exit(1)

        # Initialize the retriever
        retriever = RAGRetriever()

        # Validate embedding compatibility
        if not retriever.validate_embedding_compatibility():
            print("ERROR: Embedding compatibility validation failed")
            sys.exit(1)

        if args.validate or args.test_queries:
            # Run validation
            test_queries = args.test_queries or [
                "What are robotics fundamentals?",
                "Explain the basic principles of automation",
                "How to implement a controller system?"
            ]

            validation_results = retriever.validate_retrieval_pipeline(test_queries)

            if validation_results["validation_passed"]:
                print("\n✅ Pipeline validation PASSED")
                print(f"Overall accuracy: {validation_results['overall_accuracy']:.3f}")
            else:
                print("\n❌ Pipeline validation FAILED")
                if validation_results["issues_found"]:
                    print("Issues found:")
                    for issue in validation_results["issues_found"]:
                        print(f"  - {issue}")

        elif args.query:
            # Perform retrieval for the given query
            results = retriever.retrieve_chunks(args.query, args.top_k)

            print(f"\n📊 Results for query: '{args.query}'")
            print("="*60)

            if results:
                for chunk in results:
                    print(f"Rank {chunk['rank']}: (Score: {chunk['relevance_score']:.3f})")
                    print(f"URL: {chunk['source_url']}")
                    print(f"Section: {chunk['section']}")
                    print(f"Heading: {chunk['heading']}")
                    print(f"Content: {chunk['content'][:200]}{'...' if len(chunk['content']) > 200 else ''}")
                    print("-" * 60)
            else:
                print("No relevant chunks found for the query.")

        else:
            # Default behavior - show usage
            print("RAG Data Retrieval and Pipeline Validation")
            print("="*50)
            print("Usage examples:")
            print("  python retrieve.py \"What are robotics fundamentals?\"")
            print("  python retrieve.py --query \"Explain automation\" --top-k 3")
            print("  python retrieve.py --validate")
            print("  python retrieve.py --validate --test-queries \"query1\" \"query2\"")

    except ConfigurationError as e:
        print(f"Configuration error: {str(e)}")
        print("\nPlease ensure you have set the required environment variables:")
        print("- COHERE_API_KEY: Your Cohere API key")
        print("- QDRANT_URL: Your Qdrant Cloud URL")
        print("- QDRANT_API_KEY: Your Qdrant API key (if required)")
        sys.exit(1)
    except RetrievalError as e:
        print(f"Retrieval error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running retrieval system: {str(e)}")
        sys.exit(1)
    finally:
        # Close any resources
        try:
            retriever.close()
        except:
            pass  # Ignore errors during cleanup


if __name__ == "__main__":
    main()