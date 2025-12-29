#!/usr/bin/env python3
"""
Qdrant Book Ingestion Pipeline
Ingests an entire book into Qdrant vector database for RAG retrieval.
"""

import os
import re
import uuid
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "document_embeddings")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))


@dataclass
class BookChunk:
    chunk_id: str
    content: str
    chapter: str
    source: str
    chunk_index: int


def load_book_content(file_path: str) -> Tuple[str, str]:
    """
    Load book content from a text/markdown file or a folder of markdown files.

    Args:
        file_path: Path to the book file (.txt or .md) or folder containing .md files

    Returns:
        Tuple of (raw_text, book_name)
    """
    logger.info(f"Loading book from: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Book file/folder not found: {file_path}")

    # Check if it's a directory
    if os.path.isdir(file_path):
        return load_book_from_folder(file_path)

    book_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    logger.info(f"Loaded book '{book_name}' with {len(content)} characters")
    return content, book_name


def load_book_from_folder(folder_path: str) -> Tuple[str, str]:
    """
    Load book content from a folder containing multiple markdown files.

    Args:
        folder_path: Path to folder containing .md or .txt files

    Returns:
        Tuple of (combined_text, book_name)
    """
    book_name = os.path.basename(folder_path.rstrip('/\\'))
    all_content = []
    file_count = 0

    # Walk through folder and subfolders
    for root, dirs, files in os.walk(folder_path):
        # Sort files for consistent ordering
        for file in sorted(files):
            if file.endswith(('.md', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Add chapter marker based on folder/file structure
                    relative_path = os.path.relpath(file_path, folder_path)
                    chapter_marker = f"\n\n## File: {relative_path}\n\n"
                    all_content.append(chapter_marker + content)
                    file_count += 1
                    logger.info(f"Loaded: {relative_path}")
                except Exception as e:
                    logger.warning(f"Could not read {file_path}: {e}")

    if not all_content:
        raise ValueError(f"No .md or .txt files found in {folder_path}")

    combined_content = '\n'.join(all_content)
    logger.info(f"Loaded {file_count} files from '{book_name}' with {len(combined_content)} total characters")
    return combined_content, book_name


def chunk_book_content(
    content: str,
    book_name: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[BookChunk]:
    """
    Split book content into meaningful chunks with metadata.

    Args:
        content: Raw book text
        book_name: Name of the book for metadata
        chunk_size: Maximum characters per chunk
        chunk_overlap: Overlap between consecutive chunks

    Returns:
        List of BookChunk objects with metadata
    """
    logger.info(f"Chunking book with size={chunk_size}, overlap={chunk_overlap}")

    chapters = extract_chapters(content)
    chunks = []
    chunk_index = 0

    for chapter_name, chapter_content in chapters:
        chapter_chunks = split_into_chunks(
            chapter_content,
            chunk_size,
            chunk_overlap
        )

        for chunk_text in chapter_chunks:
            if chunk_text.strip():
                chunk = BookChunk(
                    chunk_id=str(uuid.uuid4()),
                    content=chunk_text.strip(),
                    chapter=chapter_name,
                    source=book_name,
                    chunk_index=chunk_index
                )
                chunks.append(chunk)
                chunk_index += 1

    logger.info(f"Created {len(chunks)} chunks from book")
    return chunks


def extract_chapters(content: str) -> List[Tuple[str, str]]:
    """
    Extract chapters from book content.
    Looks for common chapter patterns in markdown and text files.
    """
    chapter_patterns = [
        r'^#{1,2}\s+(.+?)$',
        r'^Chapter\s+\d+[:\s]+(.+?)$',
        r'^CHAPTER\s+\d+[:\s]+(.+?)$',
        r'^\*\*(.+?)\*\*$',
    ]

    combined_pattern = '|'.join(f'({p})' for p in chapter_patterns)

    lines = content.split('\n')
    chapters = []
    current_chapter = "Introduction"
    current_content = []

    for line in lines:
        is_chapter_header = False
        for pattern in chapter_patterns:
            match = re.match(pattern, line.strip(), re.IGNORECASE | re.MULTILINE)
            if match:
                if current_content:
                    chapters.append((current_chapter, '\n'.join(current_content)))

                current_chapter = match.group(1) if match.group(1) else line.strip()
                current_chapter = re.sub(r'^#+\s*', '', current_chapter)
                current_content = []
                is_chapter_header = True
                break

        if not is_chapter_header:
            current_content.append(line)

    if current_content:
        chapters.append((current_chapter, '\n'.join(current_content)))

    if not chapters:
        chapters = [("Full Book", content)]

    return chapters


def split_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Split text into overlapping chunks, respecting sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))

            overlap_text = ' '.join(current_chunk)
            overlap_start = max(0, len(overlap_text) - overlap)
            overlap_content = overlap_text[overlap_start:]

            current_chunk = [overlap_content] if overlap_content.strip() else []
            current_length = len(overlap_content)

        current_chunk.append(sentence)
        current_length += sentence_length + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def generate_embeddings(
    chunks: List[BookChunk],
    batch_size: int = 96
) -> List[Tuple[BookChunk, List[float]]]:
    """
    Generate vector embeddings for each chunk using Cohere API.

    Args:
        chunks: List of BookChunk objects
        batch_size: Number of chunks to process per API call

    Returns:
        List of tuples (chunk, embedding_vector)
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set")

    logger.info(f"Generating embeddings for {len(chunks)} chunks")

    client = cohere.Client(COHERE_API_KEY)
    model = "embed-english-v3.0"

    results = []
    total_batches = (len(chunks) + batch_size - 1) // batch_size

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_texts = [chunk.content for chunk in batch_chunks]
        batch_num = (i // batch_size) + 1

        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch_chunks)} chunks)")

        try:
            response = client.embed(
                texts=batch_texts,
                model=model,
                input_type="search_document"
            )

            for chunk, embedding in zip(batch_chunks, response.embeddings):
                results.append((chunk, embedding))

        except Exception as e:
            logger.error(f"Error generating embeddings for batch {batch_num}: {e}")
            raise

    logger.info(f"Successfully generated {len(results)} embeddings")
    return results


def upload_to_qdrant(
    embeddings: List[Tuple[BookChunk, List[float]]],
    collection_name: str = COLLECTION_NAME
) -> int:
    """
    Upload vectors with metadata to Qdrant.

    Args:
        embeddings: List of (chunk, embedding) tuples
        collection_name: Name of the Qdrant collection

    Returns:
        Number of successfully uploaded points
    """
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set")

    logger.info(f"Connecting to Qdrant at {QDRANT_URL}")

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        https=True
    )

    points = []
    for chunk, embedding in embeddings:
        point = PointStruct(
            id=chunk.chunk_id,
            vector=embedding,
            payload={
                "text": chunk.content,
                "content": chunk.content,
                "chapter": chunk.chapter,
                "source": chunk.source,
                "chunk_index": chunk.chunk_index,
                "chunk_id": chunk.chunk_id
            }
        )
        points.append(point)

    logger.info(f"Uploading {len(points)} points to collection '{collection_name}'")

    batch_size = 100
    uploaded_count = 0

    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        try:
            client.upsert(
                collection_name=collection_name,
                points=batch,
                wait=True
            )
            uploaded_count += len(batch)
            logger.info(f"Uploaded batch {(i // batch_size) + 1}: {uploaded_count}/{len(points)} points")
        except Exception as e:
            logger.error(f"Error uploading batch: {e}")
            raise

    logger.info(f"Successfully uploaded {uploaded_count} points to Qdrant")
    return uploaded_count


def ingest_book(
    file_path: str,
    collection_name: str = COLLECTION_NAME,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> Dict[str, Any]:
    """
    Main ingestion function - orchestrates the complete pipeline.

    Args:
        file_path: Path to the book file
        collection_name: Qdrant collection name
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        Dictionary with ingestion statistics
    """
    logger.info("=" * 50)
    logger.info("Starting Book Ingestion Pipeline")
    logger.info("=" * 50)

    stats = {
        "success": False,
        "book_name": None,
        "total_characters": 0,
        "total_chunks": 0,
        "total_embeddings": 0,
        "uploaded_points": 0,
        "collection_name": collection_name,
        "error": None
    }

    try:
        content, book_name = load_book_content(file_path)
        stats["book_name"] = book_name
        stats["total_characters"] = len(content)

        chunks = chunk_book_content(content, book_name, chunk_size, chunk_overlap)
        stats["total_chunks"] = len(chunks)

        if not chunks:
            raise ValueError("No chunks were created from the book content")

        embeddings = generate_embeddings(chunks)
        stats["total_embeddings"] = len(embeddings)

        uploaded_count = upload_to_qdrant(embeddings, collection_name)
        stats["uploaded_points"] = uploaded_count

        stats["success"] = True

        logger.info("=" * 50)
        logger.info("INGESTION COMPLETE")
        logger.info(f"  Book: {book_name}")
        logger.info(f"  Characters: {stats['total_characters']:,}")
        logger.info(f"  Chunks: {stats['total_chunks']}")
        logger.info(f"  Embeddings: {stats['total_embeddings']}")
        logger.info(f"  Uploaded: {stats['uploaded_points']}")
        logger.info(f"  Collection: {collection_name}")
        logger.info("=" * 50)

    except Exception as e:
        stats["error"] = str(e)
        logger.error(f"Ingestion failed: {e}")
        raise

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest a book into Qdrant vector database")
    parser.add_argument("file_path", help="Path to the book file (.txt or .md)")
    parser.add_argument("--collection", default=COLLECTION_NAME, help="Qdrant collection name")
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE, help="Chunk size in characters")
    parser.add_argument("--chunk-overlap", type=int, default=CHUNK_OVERLAP, help="Overlap between chunks")

    args = parser.parse_args()

    result = ingest_book(
        file_path=args.file_path,
        collection_name=args.collection,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )

    if result["success"]:
        print(f"\nSuccess! Ingested '{result['book_name']}' with {result['uploaded_points']} vectors.")
    else:
        print(f"\nFailed: {result['error']}")
