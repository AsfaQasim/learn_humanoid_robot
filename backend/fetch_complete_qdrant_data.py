#!/usr/bin/env python3
"""
Complete Python solution to fetch all data from Qdrant collection 'test_ingestion'.
Uses the scroll API to retrieve all points including IDs, vectors, and payloads.
Handles pagination automatically until all data is fetched.
"""

import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from qdrant_client.conversions import common_types as types


def get_qdrant_client() -> QdrantClient:
    """
    Create and return a configured Qdrant client using environment variables or fallback values.
    Handles both local and cloud connections.
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


def fetch_all_points_from_collection(
    client: QdrantClient,
    collection_name: str,
    batch_size: int = 100,
    with_vectors: bool = True
) -> List[Dict[str, Any]]:
    """
    Fetch all points from a Qdrant collection using the scroll API.

    Args:
        client: Configured Qdrant client
        collection_name: Name of the collection to fetch data from
        batch_size: Number of points to fetch per batch (default: 100)
        with_vectors: Whether to include vectors in the response (default: True)

    Returns:
        List of dictionaries containing point data (id, vector, payload)
    """
    print(f"[INFO] Fetching all points from collection '{collection_name}'...")
    print(f"[INFO] Batch size: {batch_size}, Include vectors: {with_vectors}")

    all_points = []
    offset = None  # Start with no offset
    batch_num = 0

    try:
        # Get collection info to show total count
        collection_info = client.get_collection(collection_name)
        total_points = collection_info.points_count
        print(f"[INFO] Collection '{collection_name}' contains {total_points} points")

        while True:
            batch_num += 1
            print(f"[INFO] Fetching batch {batch_num} (offset: {offset})...")

            # Use scroll API to get points
            records, next_offset = client.scroll(
                collection_name=collection_name,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=with_vectors
            )

            # Convert records to dictionaries
            for record in records:
                point_data = {
                    "id": record.id,
                    "payload": record.payload,
                    "vector": record.vector if record.vector else None
                }
                all_points.append(point_data)

            # Check if we've reached the end
            if next_offset is None:
                print(f"[INFO] Reached end of collection. Fetched {len(all_points)} points in total.")
                break

            # Update offset for next iteration
            offset = next_offset

            # Progress indicator
            print(f"[INFO] Fetched {len(all_points)}/{total_points} points ({len(all_points)/total_points*100:.1f}%)")

            # Safety check to avoid infinite loops
            if len(all_points) >= total_points:
                print(f"[INFO] Reached expected total points count. Stopping.")
                break

        return all_points

    except Exception as e:
        print(f"[ERROR] Error fetching data from collection '{collection_name}': {e}")
        raise


def print_point_sample(points: List[Dict[str, Any]], num_samples: int = 3) -> None:
    """
    Print a sample of the fetched points for inspection.

    Args:
        points: List of point data dictionaries
        num_samples: Number of samples to print (default: 3)
    """
    print(f"\n[INFO] Sample of {min(num_samples, len(points))} points:")

    for i, point in enumerate(points[:num_samples]):
        print(f"\n--- Point {i+1} ---")
        print(f"ID: {point['id']}")
        print(f"Payload keys: {list(point['payload'].keys()) if point['payload'] else 'None'}")
        print(f"Vector type: {type(point['vector'])}")
        if point['vector']:
            vector_len = len(point['vector']) if isinstance(point['vector'], (list, tuple)) else 'N/A'
            print(f"Vector length: {vector_len}")

        # Print payload content (first few items)
        if point['payload']:
            print("Payload sample:")
            payload_items = list(point['payload'].items())[:3]  # Show first 3 items
            for key, value in payload_items:
                value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                print(f"  {key}: {value_str}")


def save_points_to_file(points: List[Dict[str, Any]], filename: str = "qdrant_data.json") -> None:
    """
    Save the fetched points to a JSON file.

    Args:
        points: List of point data dictionaries
        filename: Output filename (default: "qdrant_data.json")
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(points, f, indent=2, default=str)
        print(f"[INFO] Data saved to {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save data to file: {e}")


def main():
    """
    Main function to fetch all data from the test_ingestion collection.
    """
    print("[INFO] Starting complete Qdrant data fetcher for 'test_ingestion' collection")

    # Create Qdrant client
    client = get_qdrant_client()

    try:
        # Check if the target collection exists
        collection_name = "test_ingestion"
        try:
            collection_info = client.get_collection(collection_name)
            print(f"[INFO] Collection '{collection_name}' exists with {collection_info.points_count} points")
        except Exception as e:
            print(f"[ERROR] Collection '{collection_name}' not found: {e}")
            print("[INFO] Available collections:")
            collections = client.get_collections().collections
            for col in collections:
                print(f"  - {col.name}")
            return

        # Fetch all points from the collection
        all_points = fetch_all_points_from_collection(
            client=client,
            collection_name=collection_name,
            batch_size=100,  # Adjust based on your memory constraints
            with_vectors=True  # Set to False if you don't need vectors to save memory
        )

        print(f"\n[SUCCESS] Successfully fetched {len(all_points)} points from '{collection_name}'")

        # Print a sample of the data
        if all_points:
            print_point_sample(all_points, num_samples=min(5, len(all_points)))
        else:
            print(f"[INFO] No points found in collection '{collection_name}'")

        # Optionally save to file
        save_choice = input("\nDo you want to save the data to a JSON file? (y/n): ").lower().strip()
        if save_choice == 'y':
            filename = input("Enter filename (default: qdrant_data.json): ").strip()
            if not filename:
                filename = "qdrant_data.json"
            save_points_to_file(all_points, filename)

        return all_points

    except Exception as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    data = main()