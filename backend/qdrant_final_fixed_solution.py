#!/usr/bin/env python3
"""
FINAL CORRECTED SOLUTION: Complete RAG implementation for Qdrant v1.16.2+
This fixes the 'QdrantClient' object has no attribute 'search' error.
"""

import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from qdrant_client import QdrantClient


def get_qdrant_client() -> QdrantClient:
    """Create and return a configured Qdrant client."""
    load_dotenv()

    qdrant_url = os.getenv("QDRANT_URL") or os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_port = os.getenv("QDRANT_PORT", "6333")

    if qdrant_url is None or qdrant_url.lower() in ["localhost", "127.0.0.1", ""]:
        print("[INFO] Connecting to local Qdrant instance...")
        client = QdrantClient(host="localhost", port=int(qdrant_port))
    elif qdrant_api_key:
        print(f"[INFO] Connecting to Qdrant cloud at: {qdrant_url}")
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    else:
        print(f"[INFO] Connecting to Qdrant at: {qdrant_url}")
        client = QdrantClient(url=qdrant_url)

    return client


def search_chunks_for_rag(client: QdrantClient, collection_name: str, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    CORRECT METHOD: Fetch relevant chunks for RAG using query_points() method (v1.16.2+).
    The new API uses query_points() for vector-based similarity search.
    """
    print(f"[INFO] Performing RAG search in '{collection_name}'...")

    try:
        # ✅ CORRECT: Use query_points() method for vector-based search in v1.16.2+
        search_results = client.query_points(
            collection_name=collection_name,
            query=query_vector,  # Vector as the query parameter
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )

        results = []
        for hit in search_results.points:
            results.append({
                'id': hit.id,
                'payload': hit.payload,
                'score': hit.score
            })

        print(f"[SUCCESS] Found {len(results)} relevant chunks")
        return results

    except Exception as e:
        print(f"[ERROR] RAG search failed: {e}")
        raise


def fetch_all_collection_data(client: QdrantClient, collection_name: str, batch_size: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch all data from collection using scroll() method (unchanged in v1.16.2+).
    """
    print(f"[INFO] Fetching ALL data from '{collection_name}'...")

    all_points = []
    offset = None

    try:
        while True:
            records, next_offset = client.scroll(
                collection_name=collection_name,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=True
            )

            for record in records:
                all_points.append({
                    'id': record.id,
                    'payload': record.payload,
                    'vector': record.vector
                })

            if next_offset is None:
                break
            offset = next_offset

        print(f"[SUCCESS] Fetched {len(all_points)} total points")
        return all_points

    except Exception as e:
        print(f"[ERROR] Fetch all data failed: {e}")
        raise


def main():
    """Main function demonstrating the fix for the search error."""
    print("FIXED: Qdrant RAG Implementation for v1.16.2+")
    print("="*50)
    print("ERROR FIXED: Replaced client.search() with client.query_points()")
    print()

    client = get_qdrant_client()
    collection_name = "test_ingestion"

    try:
        # Verify collection exists
        collection_info = client.get_collection(collection_name)
        print(f"[INFO] Collection '{collection_name}' has {collection_info.points_count} points")

        # Determine vector size from collection
        vector_size = collection_info.config.params.vectors.size if hasattr(collection_info.config.params, 'vectors') else 1536

        # Create a sample query vector (in practice, this would come from your embedding model)
        query_vector = [0.1] * vector_size  # Replace with actual embedding of user question

        # ✅ CORRECT USAGE: Use query_points() instead of search()
        results = search_chunks_for_rag(client, collection_name, query_vector, top_k=3)

        print("\n[RELEVANT CHUNKS FOUND:]")
        for i, chunk in enumerate(results, 1):
            print(f"  {i}. ID: {chunk['id']}, Score: {chunk['score']}")
            print(f"     Content: {str(chunk['payload'])[:100]}...")

        print(f"\n[SUCCESS] RAG search completed without 'search' attribute error!")
        print(f"[INFO] Your Qdrant client version supports the new API.")

    except AttributeError as e:
        if "'QdrantClient' object has no attribute 'search'" in str(e):
            print("[ERROR] You're still trying to use client.search() somewhere in your code!")
            print("SOLUTION: Replace ALL instances of client.search() with client.query_points()")
        else:
            print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()