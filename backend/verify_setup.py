"""
Verify that the correct code is loaded before starting the server.
"""
import sys
import os

print("=" * 70)
print("VERIFYING BACKEND SETUP")
print("=" * 70)

# Check 1: qdrant_compat exists
print("\n1. Checking qdrant_compat.py...")
if os.path.exists("qdrant_compat.py"):
    print("   [OK] qdrant_compat.py exists")
else:
    print("   [ERROR] qdrant_compat.py NOT FOUND")
    sys.exit(1)

# Check 2: Can import qdrant_compat
print("\n2. Testing import of qdrant_compat...")
try:
    from qdrant_compat import safe_qdrant_search
    print("   [OK] qdrant_compat imports successfully")
except Exception as e:
    print(f"   [ERROR] Cannot import qdrant_compat: {e}")
    sys.exit(1)

# Check 3: Check rag_service uses compatibility layer
print("\n3. Checking rag_service.py uses compatibility layer...")
with open("rag_service.py", "r", encoding="utf-8") as f:
    content = f.read()
    if "from qdrant_compat import safe_qdrant_search" in content:
        print("   [OK] rag_service.py imports qdrant_compat")
    else:
        print("   [ERROR] rag_service.py does NOT import qdrant_compat")
        sys.exit(1)

    if "safe_qdrant_search(" in content:
        print("   [OK] rag_service.py uses safe_qdrant_search()")
    else:
        print("   [ERROR] rag_service.py does NOT use safe_qdrant_search()")
        sys.exit(1)

# Check 4: Verify VERSION 2.0 marker exists
print("\n4. Checking for VERSION 2.0 marker...")
if "VERSION 2.0" in content:
    print("   [OK] VERSION 2.0 marker found")
else:
    print("   [ERROR] VERSION 2.0 marker NOT FOUND")
    sys.exit(1)

print("\n" + "=" * 70)
print("[SUCCESS] ALL CHECKS PASSED - Setup is correct!")
print("=" * 70)
print("\nYou can now start the server with: python run_server.py")
