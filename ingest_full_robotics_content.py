#!/usr/bin/env python3
"""
Script to ingest full content from the Physical AI & Humanoid Robotics website
into the RAG system.

This script will:
1. Scrape content from multiple pages of the target website
2. Process and embed the content
3. Store it in Qdrant for retrieval
"""

import os
import sys
from typing import List

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from backend.src.scraper import DocumentScraper
from backend.src.chunker import TextChunker
from backend.src.embeddings import EmbeddingGenerator
from backend.src.storage import VectorStorage
from backend.src.config import config
from backend.src.logging_config import logger


def main():
    """Main function to ingest content from the Physical AI & Humanoid Robotics website."""
    print("[START] Starting ingestion of Physical AI & Humanoid Robotics website content...")
    print("[INFO] Target website: https://learn-humanoid-robot.vercel.app/")

    # Check if required environment variables are set
    if not config.COHERE_API_KEY or config.COHERE_API_KEY == "your-cohere-api-key-here":
        print("[ERROR] COHERE_API_KEY not set properly in .env file")
        print("   Please update your .env file with a valid Cohere API key")
        return

    if not config.QDRANT_URL or config.QDRANT_URL == "your-qdrant-url-here":
        print("[ERROR] QDRANT_URL not set properly in .env file")
        print("   Please update your .env file with a valid Qdrant URL")
        return

    # URLs to scrape from the Physical AI & Humanoid Robotics website
    base_url = "https://learn-humanoid-robot.vercel.app/"

    # Specific URLs from the sitemap that were identified as relevant
    urls = [
        base_url,
        f"{base_url}docs/intro",
        f"{base_url}docs/robotics-module-one/",
        f"{base_url}docs/robotics-module-one/chapter-1/lesson-1",
        f"{base_url}docs/robotics-module-one/chapter-1/lesson-2",
        f"{base_url}docs/robotics-module-one/chapter-1/lesson-3",
        f"{base_url}docs/robotics-module-one/chapter-2/lesson-1",
        f"{base_url}docs/robotics-module-one/chapter-2/lesson-2",
        f"{base_url}docs/robotics-module-one/chapter-2/lesson-3",
        f"{base_url}docs/robotics-module-one/chapter-3/lesson-1",
        f"{base_url}docs/robotics-module-one/chapter-3/lesson-2",
        f"{base_url}docs/robotics-module-one/chapter-3/lesson-3",
        f"{base_url}docs/robotics-module-one/chapter-4/lesson-1",
        f"{base_url}docs/robotics-module-one/chapter-4/lesson-2",
        f"{base_url}docs/robotics-module-one/chapter-4/lesson-3",
    ]

    print(f"[INFO] Found {len(urls)} URLs to process")
    for i, url in enumerate(urls):
        print(f"  {i+1:2d}. {url}")

    # Confirm with user before proceeding
    response = input(f"\nProceed with ingesting content from {len(urls)} URLs? (y/N): ")
    if response.lower() != 'y':
        print("[ERROR] Ingestion cancelled by user")
        return

    try:
        # Initialize pipeline components
        print("\n[INFO] Initializing pipeline components...")
        chunker = TextChunker()
        embedding_generator = EmbeddingGenerator()
        vector_storage = VectorStorage()

        # Execute the pipeline
        print(f"\n[INFO] Scraping content from {len(urls)} URLs...")
        scraper = DocumentScraper()
        scraped_results = scraper.crawl_and_extract(urls)

        all_chunks = []
        for i, (metadata_record, chunks) in enumerate(scraped_results):
            print(f"  [{i+1}/{len(scraped_results)}] Extracted {len(chunks)} chunks from {metadata_record.source_url}")
            all_chunks.extend(chunks)

        if not all_chunks:
            print("[WARNING] No content extracted from URLs. Pipeline completed with no vectors stored.")
            return

        print(f"[INFO] Total chunks after scraping: {len(all_chunks)}")

        # Chunk the extracted content if needed
        print("[INFO] Processing chunks to ensure proper size...")
        final_chunks = []

        for i, doc_chunk in enumerate(all_chunks):
            if len(doc_chunk.content) > config.CHUNK_SIZE:
                sub_chunks = chunker.chunk_text(
                    text=doc_chunk.content,
                    source_url=doc_chunk.source_url,
                    section=doc_chunk.section,
                    heading=doc_chunk.heading,
                    metadata=doc_chunk.metadata
                )
                final_chunks.extend(sub_chunks)
                print(f"  [{i+1}/{len(all_chunks)}] Split large chunk into {len(sub_chunks)} sub-chunks")
            else:
                final_chunks.append(doc_chunk)
                print(f"  [{i+1}/{len(all_chunks)}] Kept chunk as is")

        print(f"[INFO] Final chunks after processing: {len(final_chunks)}")

        # Generate embeddings for chunks
        print(f"[INFO] Generating embeddings for {len(final_chunks)} chunks...")
        if final_chunks:
            embeddings = embedding_generator.generate_embeddings_from_chunks(final_chunks)
            print(f"[SUCCESS] Generated {len(embeddings)} embeddings")
        else:
            print("[WARNING] No chunks to generate embeddings for")
            embeddings = []

        # Store embeddings in vector database
        print(f"[INFO] Storing {len(embeddings)} embeddings in vector database...")
        if embeddings:
            success = vector_storage.store_embeddings(embeddings)
            if success:
                print(f"[SUCCESS] Successfully stored {len(embeddings)} embeddings in vector database")
            else:
                print("[ERROR] Failed to store embeddings in vector database")
                return
        else:
            print("[WARNING] No embeddings to store")

        # Verify storage
        print("[INFO] Verifying storage...")
        storage_ok = vector_storage.verify_storage()
        if storage_ok:
            print("[SUCCESS] Storage verification successful")
        else:
            print("[ERROR] Storage verification failed")
            return

        print(f"\n[SUCCESS] Successfully processed content from {len(urls)} URLs and stored {len(embeddings)} vectors in the database!")
        print("[INFO] The RAG system is now ready to answer questions about Physical AI & Humanoid Robotics!")

    except Exception as e:
        print(f"[ERROR] Error during ingestion: {str(e)}")
        logger.error(f"Pipeline failed with error: {str(e)}")
    finally:
        # Cleanup resources
        try:
            scraper.close()
            print("[INFO] Resources cleaned up")
        except:
            pass


if __name__ == "__main__":
    main()