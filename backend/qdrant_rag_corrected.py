#!/usr/bin/env python3
"""
Correct implementation for Qdrant client version 1.16.2+ with new API.
"""

import os
import random
from typing import List, Dict, Any
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue
from qdrant_client.models import VectorParams


def get_qdrant_client() -> QdrantClient:
    """
    Create and return a configured Qdrant client.
    """
    load_dotenv()

    # Try to get configuration from environment variables
    qdrant_url = os.getenv("QDRANT_URL") or os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_port = os.getenv("QDRANT_PORT", "6333")

    # Check if we should connect to local Qdrant
    if qdrant_url is None or qdrant_url.lower() in ["localhost", "127.0.0.1", ""]:
        print("[INFO] Connecting to local Qdrant instance...")
        client = QdrantClient(host="localhost", port=int(qdrant_port))
    elif qdrant_api_key:
        # Cloud connection with API key
        print(f"[INFO] Connecting to Qdrant cloud at: {qdrant_url}")
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
    else:
        # Local connection without API key
        print(f"[INFO] Connecting to Qdrant at: {qdrant_url}")
        client = QdrantClient(url=qdrant_url)

    return client


def search_relevant_chunks(client: QdrantClient, collection_name: str, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch relevant chunks for a user question using similarity search.
    In newer versions (1.16.2+), use the query method instead of search.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to search in
        query_vector: Vector representation of the user's question
        top_k: Number of top results to return

    Returns:
        List of relevant chunks with payload and scores
    """
    print(f"[INFO] Searching for relevant chunks in '{collection_name}'...")

    try:
        # Use query method (correct method name in newer versions 1.16.2+)
        search_results = client.query(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )

        # Convert results to a more usable format
        results = []
        for hit in search_results:
            results.append({
                'id': hit.id,
                'payload': hit.payload,
                'score': hit.score
            })

        print(f"[INFO] Found {len(results)} relevant chunks")
        return results

    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        raise


def fetch_all_data_from_collection(client: QdrantClient, collection_name: str, batch_size: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch complete data from the collection using scroll method.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to fetch data from
        batch_size: Number of points to fetch per batch

    Returns:
        List of all points in the collection
    """
    print(f"[INFO] Fetching all data from '{collection_name}' using scroll...")

    all_points = []
    offset = None
    batch_num = 0

    try:
        while True:
            batch_num += 1
            print(f"[INFO] Fetching batch {batch_num}...")

            # Use scroll method (this still exists in newer versions)
            records, next_offset = client.scroll(
                collection_name=collection_name,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=True
            )

            # Add records to our collection
            for record in records:
                point_data = {
                    'id': record.id,
                    'payload': record.payload,
                    'vector': record.vector
                }
                all_points.append(point_data)

            # Check if we've reached the end
            if next_offset is None:
                print(f"[INFO] Reached end of collection. Fetched {len(all_points)} points in total.")
                break

            # Update offset for next iteration
            offset = next_offset

            # Safety check to avoid infinite loops
            collection_info = client.get_collection(collection_name)
            if len(all_points) >= collection_info.points_count:
                print(f"[INFO] Reached expected total points count. Stopping.")
                break

        return all_points

    except Exception as e:
        print(f"[ERROR] Fetching all data failed: {e}")
        raise


def create_rag_chatbot():
    """
    Example RAG chatbot implementation using correct Qdrant methods for version 1.16.2+.
    """
    print("[INFO] Initializing RAG Chatbot with Qdrant (v1.16.2+ API)...")

    # Initialize client
    client = get_qdrant_client()
    collection_name = "test_ingestion"

    try:
        # Test connection by checking if collection exists
        collection_info = client.get_collection(collection_name)
        print(f"[INFO] Collection '{collection_name}' exists with {collection_info.points_count} points")

        # Example: Simulate a user question (you would convert the actual question to a vector using an embedding model)
        # For demonstration, using a random vector - adjust dimensions to match your collection
        # You should get the vector size from your collection configuration
        vector_size = collection_info.config.params.vectors.size if hasattr(collection_info.config.params, 'vectors') else 1536
        query_vector = [random.random() for _ in range(vector_size)]

        # Step 1: Search for relevant chunks using the NEW query method
        relevant_chunks = search_relevant_chunks(client, collection_name, query_vector, top_k=5)

        # Print results
        print("\n[INFO] Relevant chunks found:")
        for i, chunk in enumerate(relevant_chunks, 1):
            print(f"  {i}. ID: {chunk['id']}")
            print(f"     Score: {chunk['score']}")
            print(f"     Content: {str(chunk['payload'])[:100]}...")

        # Step 2: Example of fetching all data (for initial data exploration)
        fetch_all_choice = input("\nDo you want to fetch ALL data from the collection? (y/n): ").lower().strip()
        if fetch_all_choice == 'y':
            all_data = fetch_all_data_from_collection(client, collection_name)
            print(f"\n[SUCCESS] Fetched {len(all_data)} total points from collection")

        return relevant_chunks

    except Exception as e:
        print(f"[ERROR] RAG chatbot failed: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """
    Main function demonstrating correct Qdrant usage for version 1.16.2+.
    """
    print("Qdrant RAG Implementation - Correct Methods for v1.16.2+")
    print("=" * 60)

    # Run the RAG chatbot example
    results = create_rag_chatbot()

    print(f"\n[INFO] RAG process completed. Found {len(results)} relevant chunks.")


if __name__ == "__main__":
    main()