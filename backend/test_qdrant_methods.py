#!/usr/bin/env python3
"""
Simple test script to verify Qdrant client methods are working correctly.
"""

from qdrant_client import QdrantClient

# Check version using importlib
import importlib.metadata
try:
    version = importlib.metadata.version('qdrant-client')
    print(f"Qdrant Client Version: {version}")
except importlib.metadata.PackageNotFoundError:
    print("Could not determine Qdrant Client version")

# Create a mock client (not connecting to anything real)
# This is just to check method availability
client = QdrantClient(":memory:")  # In-memory client for testing

# Check if the search method exists
if hasattr(client, 'search'):
    print("OK 'search' method exists")
else:
    print("ERROR 'search' method does NOT exist")

if hasattr(client, 'search_points'):
    print("OK 'search_points' method exists")
else:
    print("ERROR 'search_points' method does NOT exist")

if hasattr(client, 'scroll'):
    print("OK 'scroll' method exists")
else:
    print("ERROR 'scroll' method does NOT exist")

if hasattr(client, 'scroll_points'):
    print("OK 'scroll_points' method exists")
else:
    print("ERROR 'scroll_points' method does NOT exist")

# List all available methods that contain 'search' or 'scroll'
methods = [method for method in dir(client) if not method.startswith('_')]
search_methods = [method for method in methods if 'search' in method.lower()]
scroll_methods = [method for method in methods if 'scroll' in method.lower()]

print(f"\nSearch-related methods: {search_methods}")
print(f"Scroll-related methods: {scroll_methods}")

# Test the correct usage
print("\nCorrect usage examples:")
print("For search: client.search(collection_name='your_collection', query_vector=vector, limit=5)")
print("For scroll: client.scroll(collection_name='your_collection', limit=100, offset=None)")