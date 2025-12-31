"""
Test the exact query syntax for Qdrant client 1.8.0
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import cohere

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

print("Initializing clients...")
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, https=True)
cohere_client = cohere.Client(COHERE_API_KEY)

print("Generating test embedding...")
response = cohere_client.embed(
    texts=["test query"],
    model="embed-english-v3.0",
    input_type="search_query"
)
vector = response.embeddings[0]

print(f"Vector dimensions: {len(vector)}")

# Test 1: Using query() method
print("\n=== Test 1: Using query() method ===")
try:
    results = qdrant.query(
        collection_name="document_embeddings",
        query_vector=vector,
        limit=2,
        with_payload=True
    )
    print(f"SUCCESS! Got {len(results)} results")
    print(f"Result type: {type(results)}")
    if results:
        print(f"First result type: {type(results[0])}")
        print(f"First result attributes: {dir(results[0])[:10]}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 2: Using search() method (old API)
print("\n=== Test 2: Using search() method (old API) ===")
try:
    results = qdrant.search(
        collection_name="document_embeddings",
        query_vector=vector,
        limit=2,
        with_payload=True
    )
    print(f"SUCCESS! Got {len(results)} results")
    print(f"Result type: {type(results)}")
except Exception as e:
    print(f"FAILED: {e}")

print("\nTest complete!")
