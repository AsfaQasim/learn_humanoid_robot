"""
Test script to verify Qdrant client methods are available.
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print("Testing Qdrant Client...")
print(f"URL: {QDRANT_URL}")
print(f"API Key: {'*' * 20 if QDRANT_API_KEY else 'NOT SET'}\n")

# Initialize client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    https=True
)

print("Client initialized successfully!")
print(f"Client type: {type(client)}")
print(f"Client module: {client.__class__.__module__}\n")

# Check available methods
print("Checking available methods:")
print(f"  - has 'search': {hasattr(client, 'search')}")
print(f"  - has 'query': {hasattr(client, 'query')}")
print(f"  - has 'query_points': {hasattr(client, 'query_points')}")
print(f"  - has 'search_batch': {hasattr(client, 'search_batch')}")
print(f"  - has 'query_batch_points': {hasattr(client, 'query_batch_points')}\n")

# List all methods that contain 'search' or 'query'
print("All search/query related methods:")
for attr in dir(client):
    if 'search' in attr.lower() or 'query' in attr.lower():
        print(f"  - {attr}")

print("\nTest complete!")
