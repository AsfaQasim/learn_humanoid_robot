#!/usr/bin/env python3
"""
Script to pre-download embedding models to avoid connection issues during runtime.
"""

import os
import logging
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_embedding_model():
    """Download the embedding model to local cache"""
    model_name = "all-MiniLM-L6-v2"
    cache_folder = "./model_cache"

    logger.info(f"Starting download of embedding model: {model_name}")

    try:
        # Set environment variables to optimize download
        os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'

        # Import and configure huggingface_hub settings
        import huggingface_hub
        huggingface_hub.utils._http.BACKOFF_MAX = 2  # Reduce max backoff time

        # Download and cache the model
        model = SentenceTransformer(
            model_name,
            cache_folder=cache_folder,
            trust_remote_code=True
        )

        logger.info(f"Successfully downloaded and cached embedding model: {model_name}")

        # Test the model
        test_embedding = model.encode(["This is a test sentence"])
        logger.info(f"Model test successful. Embedding shape: {test_embedding.shape}")

        return True

    except Exception as e:
        logger.error(f"Error downloading embedding model: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = download_embedding_model()
    if success:
        logger.info("Embedding model download completed successfully!")
    else:
        logger.error("Embedding model download failed!")
        exit(1)