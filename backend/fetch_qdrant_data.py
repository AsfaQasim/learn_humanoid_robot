#!/usr/bin/env python3
"""
Script to fetch all data from Qdrant cloud database.
This script connects to your Qdrant instance and retrieves collections and data.
"""

import os
import json
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Filter

# Load environment variables
load_dotenv()

def get_qdrant_client():
    """
    Create and return a configured Qdrant client using environment variables or fallback values
    """
    qdrant_url = os.getenv("QDRANT_URL") or os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_url and qdrant_api_key:
        # Clean up the URL by removing extra spaces and text
        cleaned_url = qdrant_url.strip()
        # Remove any extra text after the URL (like "(local)")
        if "(local)" in cleaned_url:
            cleaned_url = cleaned_url.split("(local)")[0].strip()
        if "(cloud)" in cleaned_url:
            cleaned_url = cleaned_url.split("(cloud)")[0].strip()

        # Check if the URL is for localhost vs cloud - if localhost URL but has cloud API key,
        # or if the URL doesn't contain cloud.qdrant.io, use fallback cloud settings
        if ("localhost" in cleaned_url or "127.0.0.1" in cleaned_url) and len(qdrant_api_key) > 50:
            # This looks like a configuration mismatch - local URL with cloud API key
            print("[INFO] Configuration mismatch detected: local URL with cloud API key. Using cloud fallback instead.")
            fallback_url = "https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333"
            print(f"[INFO] Connecting to Qdrant cloud at: {fallback_url}")
            client = QdrantClient(
                url=fallback_url,
                api_key=qdrant_api_key,  # Use the API key from environment
            )
        else:
            print(f"[INFO] Connecting to Qdrant at: {cleaned_url}")
            client = QdrantClient(
                url=cleaned_url,
                api_key=qdrant_api_key,
            )
    else:
        # Fallback to hardcoded values if environment variables are not set
        print("[INFO] Environment variables not found. Using fallback values (check your .env file)")
        # Use the correct fallback URL (cloud instance)
        fallback_url = "https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333"
        fallback_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.cNySe9pbHewVBDaZXEUTGhpyWadhc3kWG5LWDTh51r0"
        print(f"[INFO] Using fallback URL: {fallback_url}")
        client = QdrantClient(
            url=fallback_url,
            api_key=fallback_api_key,
        )

    return client

def fetch_all_collections(client):
    """
    Fetch and display all collections in the Qdrant instance
    """
    print("\n[INFO] Fetching all collections...")
    try:
        collections_response = client.get_collections()
        collections = collections_response.collections

        print(f"\n[INFO] Found {len(collections)} collection(s):")
        collection_names = []
        for i, collection in enumerate(collections, 1):
            print(f"  {i}. {collection.name}")
            # Get detailed collection info to get points count
            try:
                collection_info = client.get_collection(collection.name)
                print(f"     Points count: {collection_info.points_count}")
                if hasattr(collection_info.config.params, 'vectors'):
                    vector_size = collection_info.config.params.vectors.size
                else:
                    vector_size = 'N/A'
                print(f"     Vector size: {vector_size}")
            except Exception as e:
                print(f"     [ERROR] Could not get detailed info: {e}")
            print()
            collection_names.append(collection.name)

        return collection_names
    except Exception as e:
        print(f"[ERROR] Error fetching collections: {e}")
        return []

def fetch_collection_data(client, collection_name, limit=10):
    """
    Fetch sample data from a specific collection
    """
    print(f"\n[INFO] Fetching sample data from collection '{collection_name}' (limit: {limit})...")
    try:
        # Get the collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection '{collection_name}' details:")
        print(f"  Points count: {collection_info.points_count}")
        print(f"  Vector size: {collection_info.config.params.vectors.size}")

        # Fetch points from the collection
        records, _ = client.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )

        print(f"\n[INFO] Sample of {min(limit, len(records))} records from '{collection_name}':")
        for i, record in enumerate(records, 1):
            print(f"  Record {i}:")
            print(f"    ID: {record.id}")
            if record.payload:
                print(f"    Payload: {json.dumps(record.payload, indent=6, default=str)}")
            print()

        return records
    except Exception as e:
        print(f"[ERROR] Error fetching data from collection '{collection_name}': {e}")
        return []

def fetch_all_data_summary(client):
    """
    Fetch a summary of all data in Qdrant
    """
    print("\n[INFO] Fetching summary of all data...")
    try:
        collections_response = client.get_collections()
        collections = collections_response.collections

        total_points = 0
        print(f"\n[INFO] Summary:")
        for collection in collections:
            # Get detailed collection info to get points count
            collection_info = client.get_collection(collection.name)
            points_count = collection_info.points_count
            print(f"  Collection '{collection.name}': {points_count} points")
            total_points += points_count

        print(f"\n[INFO] Total points across all collections: {total_points}")
        return total_points
    except Exception as e:
        print(f"[ERROR] Error fetching data summary: {e}")
        return 0


def fetch_all_points_from_collection(client, collection_name, batch_size=100, with_vectors=True):
    """
    Fetch ALL points from a specific collection using the scroll API.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to fetch data from
        batch_size: Number of points to fetch per batch (default: 100)
        with_vectors: Whether to include vectors in the response (default: True)

    Returns:
        List of all points from the collection
    """
    print(f"\n[INFO] Fetching ALL data from collection '{collection_name}'...")

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

            # Add records to our collection
            all_points.extend([{
                'id': record.id,
                'payload': record.payload,
                'vector': record.vector
            } for record in records])

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


def fetch_test_ingestion_data(client):
    """
    Specifically fetch all data from the 'test_ingestion' collection.
    """
    collection_name = "test_ingestion"
    print(f"\n[INFO] Fetching complete data from '{collection_name}' collection...")

    try:
        # Check if collection exists
        collection_info = client.get_collection(collection_name)
        print(f"[INFO] Collection '{collection_name}' found with {collection_info.points_count} points")

        # Fetch all points from the collection
        all_points = fetch_all_points_from_collection(client, collection_name)

        print(f"\n[SUCCESS] Successfully retrieved {len(all_points)} points from '{collection_name}'")

        # Display sample of the data
        if all_points:
            print(f"\n[INFO] Sample of first 3 points from '{collection_name}':")
            for i, point in enumerate(all_points[:3], 1):
                print(f"  Point {i}:")
                print(f"    ID: {point['id']}")
                print(f"    Payload keys: {list(point['payload'].keys()) if point['payload'] else 'None'}")
                if point['vector']:
                    vector_len = len(point['vector']) if isinstance(point['vector'], (list, tuple)) else 'N/A'
                    print(f"    Vector length: {vector_len}")
                print()

        return all_points

    except Exception as e:
        print(f"[ERROR] Collection '{collection_name}' not found or error occurred: {e}")
        return []

def main():
    """
    Main function to fetch and display Qdrant data
    """
    print("[INFO] Starting Qdrant Data Fetcher")

    # Create Qdrant client
    client = get_qdrant_client()

    try:
        # Test connection by getting collections
        print("\n[INFO] Testing connection to Qdrant...")
        collections = fetch_all_collections(client)

        if not collections:
            print("[WARNING] No collections found or connection failed.")
            return

        # Fetch summary of all data
        fetch_all_data_summary(client)

        # Fetch sample data from each collection
        for collection_name in collections:
            fetch_collection_data(client, collection_name, limit=5)  # Limit to 5 records per collection for readability

    except Exception as e:
        print(f"[ERROR] Connection error: {e}")
        print("\n[INFO] Make sure your QDRANT_URL and QDRANT_API_KEY are correctly set in your .env file")
        print("Example .env file content:")
        print("# Qdrant Configuration")
        print("QDRANT_URL=your_cloud_qdrant_url")
        print("QDRANT_API_KEY=your_qdrant_api_key")
        print("# Alternative variable name (as per README)")
        print("QDRANT_HOST=your_qdrant_host")

if __name__ == "__main__":
    main()