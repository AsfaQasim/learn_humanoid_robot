import sys
import os
# Add current directory to path for relative imports
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app import app

print("Registered routes:")
for route in app.routes:
    print(f"  {route.methods} {route.path}")

print("\nTrying to import rag_service to check for errors...")
try:
    from rag_service import RAGService
    print("RAGService imported successfully")
except Exception as e:
    print(f"Error importing rag_service: {e}")

print("\nChecking if environment variables are set...")
import os
print(f"QDRANT_URL set: {bool(os.getenv('QDRANT_URL'))}")
print(f"QDRANT_API_KEY set: {bool(os.getenv('QDRANT_API_KEY'))}")
print(f"COHERE_API_KEY set: {bool(os.getenv('COHERE_API_KEY'))}")