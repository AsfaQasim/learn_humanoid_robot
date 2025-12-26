#!/usr/bin/env python3
"""
Main execution entry point for the RAG ingestion pipeline.
Orchestrates the complete pipeline from URL crawling to vector storage.
"""

import argparse
import sys
from typing import List, Tuple
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper import DocumentScraper
from src.chunker import TextChunker
from src.embeddings import EmbeddingGenerator
from src.storage import VectorStorage
from src.config import config, Config
from src.models.data_models import DocumentChunk, VectorRepresentation
from src.logging_config import logger


def main():
    """Main function to orchestrate the complete ingestion pipeline."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="RAG Documentation Ingestion Pipeline")
    parser.add_argument("urls", nargs="*", help="URLs to process")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--chunk-size", type=int, help="Size of text chunks")
    parser.add_argument("--chunk-overlap", type=int, help="Overlap between chunks")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--include-sitemap", action="store_true", help="Include URLs from sitemap.xml")

    args = parser.parse_args()

    # Set up logging based on verbosity
    if args.verbose:
        from src.logging_config import setup_logging
        setup_logging(log_level="DEBUG")

    # Validate configuration with detailed validation
    if not Config.validate():
        print("[ERROR] Configuration validation failed. Please check your environment variables.")
        sys.exit(1)

    # Run detailed configuration validation
    config_errors = config.validate_config_values()
    if config_errors:
        print("[ERROR] Configuration validation errors found:")
        for error in config_errors:
            print(f"  - {error}")
        sys.exit(1)

    # Use provided URLs or default to sample URLs for testing
    urls = args.urls
    if not urls:
        print("[WARNING] No URLs provided. Using sample URLs for testing.")
        urls = [
            "https://example.com/docs/intro",  # Placeholder - replace with actual documentation URLs
            "https://example.com/docs/getting-started"
        ]
    elif args.include_sitemap and len(urls) == 1:
        # If only one URL is provided and --include-sitemap is specified, get all URLs from sitemap
        print(f"[INFO] Discovering all URLs from sitemap for: {urls[0]}")
        scraper_for_sitemap = DocumentScraper()
        urls = scraper_for_sitemap.get_all_urls(urls[0], include_sitemap=True)
        print(f"[INFO] Found {len(urls)} URLs to process from sitemap and base URL")
        scraper_for_sitemap.close()  # Clean up resources

    # Initialize pipeline components with error handling
    try:
        logger.info("Initializing pipeline components...")
        print("[INFO] Initializing pipeline components...")
        scraper = DocumentScraper()
        chunker = TextChunker(
            chunk_size=args.chunk_size or config.CHUNK_SIZE,
            overlap=args.chunk_overlap or config.CHUNK_OVERLAP
        )
        embedding_generator = EmbeddingGenerator()
        vector_storage = VectorStorage()
    except Exception as e:
        print(f"[ERROR] Failed to initialize pipeline components: {str(e)}")
        logger.error(f"Pipeline component initialization failed: {str(e)}")
        sys.exit(1)

    try:
        # Execute the pipeline
        logger.info(f"Starting ingestion pipeline for {len(urls)} URLs")

        # Step 1: Scrape URLs and extract content
        logger.info("Step 1: Scraping URLs and extracting content...")
        print(f"Processing {len(urls)} URLs...")
        scraped_results = scraper.crawl_and_extract(urls)

        all_chunks = []
        for i, (metadata_record, chunks) in enumerate(scraped_results):
            logger.info(f"Extracted {len(chunks)} chunks from {metadata_record.source_url}")
            print(f"  [{i+1}/{len(scraped_results)}] Processed {metadata_record.source_url} -> {len(chunks)} chunks")
            all_chunks.extend(chunks)

        if not all_chunks:
            logger.warning("No content extracted from URLs. Pipeline completed with no vectors stored.")
            return

        # Step 2: Chunk the extracted content
        logger.info(f"Step 2: Chunking {len(all_chunks)} extracted documents...")
        print(f"Chunking {len(all_chunks)} documents...")
        chunked_chunks = []

        for i, doc_chunk in enumerate(all_chunks):
            # Show progress
            if (i + 1) % max(1, len(all_chunks) // 10) == 0:  # Print every 10%
                print(f"  Progress: {i+1}/{len(all_chunks)} documents processed")

            # Chunk each document chunk if it's too large
            if len(doc_chunk.content) > config.CHUNK_SIZE:
                sub_chunks = chunker.chunk_text(
                    text=doc_chunk.content,
                    source_url=doc_chunk.source_url,
                    section=doc_chunk.section,
                    heading=doc_chunk.heading,
                    metadata=doc_chunk.metadata
                )
                chunked_chunks.extend(sub_chunks)
            else:
                # If the chunk is already appropriately sized, keep it as is
                chunked_chunks.append(doc_chunk)

        logger.info(f"Created {len(chunked_chunks)} final chunks after re-chunking if needed")
        print(f"Created {len(chunked_chunks)} final chunks")

        # Step 3: Generate embeddings for chunks
        logger.info("Step 3: Generating embeddings for chunks...")
        print(f"Generating embeddings for {len(chunked_chunks)} chunks...")
        if chunked_chunks:
            # Show progress during embedding generation
            embeddings = embedding_generator.generate_embeddings_from_chunks(chunked_chunks)
            logger.info(f"Generated {len(embeddings)} embeddings")
            print(f"Generated {len(embeddings)} embeddings")
        else:
            logger.warning("No chunks to generate embeddings for")
            embeddings = []
            print("No chunks to generate embeddings for")

        # Step 4: Store embeddings in vector database
        logger.info("Step 4: Storing embeddings in vector database...")
        print(f"Storing {len(embeddings)} embeddings in vector database...")
        if embeddings:
            success = vector_storage.store_embeddings(embeddings)
            if success:
                logger.info(f"Successfully stored {len(embeddings)} embeddings in vector database")
                print(f"Successfully stored {len(embeddings)} embeddings in vector database")
            else:
                logger.error("Failed to store embeddings in vector database")
                sys.exit(1)
        else:
            logger.warning("No embeddings to store")
            print("No embeddings to store")

        # Step 5: Verify storage
        logger.info("Step 5: Verifying storage...")
        print("Verifying storage...")
        storage_ok = vector_storage.verify_storage()
        if storage_ok:
            logger.info("Storage verification successful")
            print("Storage verification successful")
        else:
            logger.error("Storage verification failed")
            sys.exit(1)

        logger.info("Pipeline completed successfully!")
        print(f"Successfully processed {len(urls)} URLs and stored {len(embeddings)} vectors in the database.")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Cleanup resources
        try:
            scraper.close()
            logger.debug("Scraper resources cleaned up")
        except:
            pass  # Ignore errors during cleanup


def run_pipeline(urls: List[str]) -> bool:
    """
    Run the complete pipeline programmatically.

    Args:
        urls: List of URLs to process

    Returns:
        True if successful, False otherwise
    """
    if not urls:
        logger.warning("No URLs provided to process")
        return False

    try:
        # Initialize pipeline components
        scraper = DocumentScraper()
        chunker = TextChunker()
        embedding_generator = EmbeddingGenerator()
        vector_storage = VectorStorage()

        # Execute the pipeline
        logger.info(f"Starting ingestion pipeline for {len(urls)} URLs")

        # Step 1: Scrape URLs and extract content
        logger.info("Step 1: Scraping URLs and extracting content...")
        scraped_results = scraper.crawl_and_extract(urls)

        all_chunks = []
        for metadata_record, chunks in scraped_results:
            logger.info(f"Extracted {len(chunks)} chunks from {metadata_record.source_url}")
            all_chunks.extend(chunks)

        if not all_chunks:
            logger.warning("No content extracted from URLs")
            return True  # Not an error, just no content

        # Step 2: Chunk the extracted content
        logger.info(f"Step 2: Chunking {len(all_chunks)} extracted documents...")
        chunked_chunks = []

        for doc_chunk in all_chunks:
            # Chunk each document chunk if it's too large
            if len(doc_chunk.content) > config.CHUNK_SIZE:
                sub_chunks = chunker.chunk_text(
                    text=doc_chunk.content,
                    source_url=doc_chunk.source_url,
                    section=doc_chunk.section,
                    heading=doc_chunk.heading,
                    metadata=doc_chunk.metadata
                )
                chunked_chunks.extend(sub_chunks)
            else:
                # If the chunk is already appropriately sized, keep it as is
                chunked_chunks.append(doc_chunk)

        logger.info(f"Created {len(chunked_chunks)} final chunks after re-chunking if needed")

        # Step 3: Generate embeddings for chunks
        logger.info("Step 3: Generating embeddings for chunks...")
        if chunked_chunks:
            embeddings = embedding_generator.generate_embeddings_from_chunks(chunked_chunks)
            logger.info(f"Generated {len(embeddings)} embeddings")
        else:
            logger.warning("No chunks to generate embeddings for")
            embeddings = []

        # Step 4: Store embeddings in vector database
        logger.info("Step 4: Storing embeddings in vector database...")
        if embeddings:
            success = vector_storage.store_embeddings(embeddings)
            if success:
                logger.info(f"Successfully stored {len(embeddings)} embeddings in vector database")
            else:
                logger.error("Failed to store embeddings in vector database")
                return False
        else:
            logger.warning("No embeddings to store")

        # Step 5: Verify storage
        logger.info("Step 5: Verifying storage...")
        storage_ok = vector_storage.verify_storage()
        if storage_ok:
            logger.info("Storage verification successful")
        else:
            logger.error("Storage verification failed")
            return False

        logger.info("Pipeline completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        return False


if __name__ == "__main__":
    main()