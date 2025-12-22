"""
Configuration file for the RAG Chatbot application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Default collection name - make sure this matches your existing collection
DEFAULT_COLLECTION_NAME = "test_ingestion_custom"

# Model Configuration
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GEMINI_MODEL_NAME = "gemini-2.5-flash"

# RAG Configuration
TOP_K_RETRIEVAL = 5
MAX_OUTPUT_TOKENS = 150
TEMPERATURE = 0.7

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 0
BATCH_SIZE = 100