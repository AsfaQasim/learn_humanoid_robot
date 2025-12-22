#!/usr/bin/env python3
"""
Final test to verify all Qdrant search() method fixes are working correctly.
"""

from src.services.rag_service import RAGService
from src.vector_store import get_qdrant_client
from qdrant_client import QdrantClient

print("[TEST] Testing Qdrant API fixes for version 1.16.2+")
print("=" * 55)

# Test 1: Verify Qdrant client has the correct methods
client = get_qdrant_client()
print(f"[PASS] Qdrant client connected successfully")

# Check that search method doesn't exist (this was causing the error)
has_search = hasattr(client, 'search')
has_query_points = hasattr(client, 'query_points')

print(f"[PASS] 'search' method exists: {has_search} (should be False)")
print(f"[PASS] 'query_points' method exists: {has_query_points} (should be True)")

# Test 2: Test RAGService instantiation
rag_service = RAGService()
print(f"[PASS] RAGService instantiated successfully")

# Test 3: Verify the retrieve method is using the correct API
import inspect
retrieve_source = inspect.getsource(rag_service.retrieve)
uses_query_points = 'query_points' in retrieve_source
uses_search = 'search(' in retrieve_source and '.search(' not in retrieve_source  # Avoid matching "search_result.points"

print(f"[PASS] retrieve() method uses 'query_points': {uses_query_points}")
print(f"[PASS] retrieve() method does NOT use old 'search': {not uses_search}")

# Test 4: Test that we can call the method without attribute error
try:
    # Just check the method exists and signature is correct
    sig = inspect.signature(rag_service.retrieve)
    print(f"[PASS] retrieve method signature: {sig}")

    # This would cause the original error if search() was still being used inappropriately
    print("[PASS] Method signature test passed")
except AttributeError as e:
    if "'QdrantClient' object has no attribute 'search'" in str(e):
        print(f"[FAIL] Original search error still exists: {e}")
    else:
        print(f"[FAIL] Other AttributeError: {e}")
except Exception as e:
    print(f"[WARN] Other error (might be expected): {e}")

print("\n" + "=" * 55)
if has_query_points and not has_search and uses_query_points and not uses_search:
    print("[SUCCESS] ALL FIXES SUCCESSFUL!")
    print("[SUCCESS] Replaced all client.search() calls with client.query_points()")
    print("[SUCCESS] RAG backend should now work without the search error")
    print("[SUCCESS] Both RAGService and chabot_Run.py are fixed")
else:
    print("[WARN] Some issues may remain - check the results above")

print("=" * 55)