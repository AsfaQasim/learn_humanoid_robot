#!/usr/bin/env python3
"""
Script to ingest your actual robotics documentation from frontend/docs/robotics-module-one
into Qdrant for the RAG chatbot.
"""
import os
import sys
import glob
from pathlib import Path
import uuid
from typing import List
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import markdown
from bs4 import BeautifulSoup
import re

# Add the backend directory to the path so we can import our modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from src.config import DEFAULT_COLLECTION_NAME
from src.vector_store import get_qdrant_client


def extract_text_from_markdown(file_path: str) -> str:
    """
    Extract clean text content from a markdown file, removing headers and formatting.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML, then extract text
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, 'html.parser')

    # Remove code blocks and other elements we don't want in the embeddings
    for code_block in soup.find_all(['code', 'pre']):
        code_block.decompose()

    # Get the text content
    text = soup.get_text()

    # Clean up the text
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove excessive newlines
    text = text.strip()

    return text


def get_all_md_files(docs_dir: str) -> List[str]:
    """
    Recursively get all markdown files from the documentation directory.
    """
    md_files = []

    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    return md_files


def chunk_document(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
    """
    Split document text into chunks of specified size.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_text(text)
    return chunks


def ingest_robotics_docs_to_qdrant():
    """
    Main function to ingest all robotics documentation into Qdrant.
    """
    print("Starting ingestion of robotics documentation into Qdrant...")

    # Get the Qdrant client
    qdrant_client = get_qdrant_client()

    # Define the documentation directory
    docs_dir = os.path.join(backend_path.parent, "frontend", "docs", "robotics-module-one")

    if not os.path.exists(docs_dir):
        print(f"ERROR: Documentation directory not found: {docs_dir}")
        return False

    print(f"Scanning documentation directory: {docs_dir}")

    # Get all markdown files
    md_files = get_all_md_files(docs_dir)
    print(f"Found {len(md_files)} markdown files to process")

    if not md_files:
        print("No markdown files found to process!")
        return False

    # Load the embedding model
    print("Loading embedding model...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Prepare all points for ingestion
    all_points = []

    for i, file_path in enumerate(md_files):
        print(f"\nProcessing file {i+1}/{len(md_files)}: {file_path}")

        try:
            # Extract text from markdown
            text_content = extract_text_from_markdown(file_path)

            if not text_content.strip():
                print(f"  WARNING: File is empty or contains no text, skipping: {file_path}")
                continue

            print(f"  Extracted {len(text_content)} characters from {file_path}")

            # Chunk the document
            chunks = chunk_document(text_content)
            print(f"  Created {len(chunks)} chunks")

            # Generate embeddings for each chunk
            for j, chunk in enumerate(chunks):
                if len(chunk.strip()) < 20:  # Skip very small chunks
                    continue

                # Generate embedding
                embedding = embedding_model.encode(chunk)

                # Create a Qdrant point
                point = models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload={
                        "text": chunk,
                        "source": file_path,
                        "chunk_index": j,
                        "file_name": os.path.basename(file_path),
                        "relative_path": os.path.relpath(file_path, docs_dir)
                    },
                )

                all_points.append(point)

        except Exception as e:
            print(f"  ERROR processing file {file_path}: {e}")
            continue

    print(f"\nTotal points to upload: {len(all_points)}")

    if not all_points:
        print("No points to upload! Check your markdown files.")
        return False

    # Ensure the collection exists
    collections = qdrant_client.get_collections().collections
    collection_names = [col.name for col in collections]

    if DEFAULT_COLLECTION_NAME not in collection_names:
        print(f"Creating collection: {DEFAULT_COLLECTION_NAME}")
        qdrant_client.create_collection(
            collection_name=DEFAULT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
    else:
        print(f"Collection {DEFAULT_COLLECTION_NAME} exists, clearing it first...")
        qdrant_client.delete_collection(DEFAULT_COLLECTION_NAME)
        print(f"Recreating collection: {DEFAULT_COLLECTION_NAME}")
        qdrant_client.create_collection(
            collection_name=DEFAULT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

    # Upload in batches to handle large datasets efficiently
    batch_size = 50  # Smaller batch size for more reliable uploads
    total_points = len(all_points)
    print(f"Uploading {total_points} points in batches of {batch_size}...")

    for i in range(0, len(all_points), batch_size):
        batch = all_points[i:i + batch_size]
        qdrant_client.upsert(
            collection_name=DEFAULT_COLLECTION_NAME,
            points=batch,
        )
        print(f"  Uploaded batch {i//batch_size + 1}/{(len(all_points)-1)//batch_size + 1}")

    print(f"\n✅ Successfully uploaded {total_points} points to collection '{DEFAULT_COLLECTION_NAME}'")
    print(f"Your chatbot will now use your actual robotics documentation!")

    # Verify the upload
    try:
        collection_info = qdrant_client.get_collection(DEFAULT_COLLECTION_NAME)
        print(f"Collection '{DEFAULT_COLLECTION_NAME}' now has {collection_info.points_count} points")

        # Show a sample of the content
        sample_points = qdrant_client.scroll(
            collection_name=DEFAULT_COLLECTION_NAME,
            limit=3
        )

        print("\nSample of ingested content:")
        for i, point in enumerate(sample_points[0][:2]):  # Show first 2
            text_preview = point.payload["text"][:150] + "..." if len(point.payload["text"]) > 150 else point.payload["text"]
            print(f"  {i+1}. File: {point.payload['file_name']}")
            print(f"     Content: {text_preview}")
            print()

        return True

    except Exception as e:
        print(f"Error verifying upload: {e}")
        return True  # Still return True since upload completed


if __name__ == "__main__":
    print("Ingesting your actual robotics documentation into Qdrant...")
    success = ingest_robotics_docs_to_qdrant()

    if success:
        print("\n✅ Documentation ingestion completed successfully!")
        print("Your chatbot will now use your real robotics content from the docs folder.")
    else:
        print("\n❌ Documentation ingestion failed!")
        sys.exit(1)