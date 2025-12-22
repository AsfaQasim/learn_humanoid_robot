#!/usr/bin/env python3
"""
Demonstration of the correct Qdrant API usage for version 1.16.2+.

The error 'QdrantClient' object has no attribute 'search' occurs because:
- In older versions (< 1.9.0): use client.search()
- In newer versions (1.9.0+): use client.query() instead of client.search()
- In latest versions (1.16.2+): client.search() is removed, only client.query() exists
"""

from qdrant_client import QdrantClient

# Create a test client
client = QdrantClient(":memory:")

print("Qdrant API Changes Summary:")
print("="*50)
print("OLD (pre-1.9.0): client.search()")
print("NEW (1.9.0+):  client.query() replaces client.search()")
print("CURRENT (1.16.2+): Only client.query() exists, client.search() removed")
print()

print("Correct usage for RAG similarity search:")
print("# Instead of:")
print("# client.search(collection_name='test_ingestion', query_vector=vector, limit=5)")
print()
print("# Use:")
print("# client.query(collection_name='test_ingestion', query_vector=vector, limit=5)")
print()

print("For scrolling through all data (no change):")
print("client.scroll(collection_name='test_ingestion', limit=100, with_payload=True)")
print()

# Demonstrate the correct methods that exist
print("Available query-like methods:", [m for m in dir(client) if 'query' in m.lower()])
print("Available search-like methods:", [m for m in dir(client) if 'search' in m.lower() and m != 'search_matrix_offsets' and m != 'search_matrix_pairs'])
print()

print("EXAMPLE USAGE:")
print()

# Example of what NOT to do (this would cause your error):
print("# This would cause the error:")
print("# try:")
print("#     results = client.search(collection_name='test', query_vector=[0.1, 0.2, 0.3], limit=5)")
print("# except AttributeError as e:")
print("#     print(e)  # 'QdrantClient' object has no attribute 'search'")
print()

print("CORRECT approach for your version:")
print("results = client.query(collection_name='test', query_vector=[0.1, 0.2, 0.3], limit=5)")