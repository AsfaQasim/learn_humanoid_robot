import argparse
import uuid
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

load_dotenv()

def ingest_data(file_path: str, collection_name: str, chunk_size: int = 1000, chunk_overlap: int = 0, batch_size: int = 100):
    """
    Ingests data from a text file into a Qdrant collection with proper chunking and batching.

    Args:
        file_path (str): The path to the text file.
        collection_name (str): The name of the Qdrant collection.
        chunk_size (int): Size of text chunks (default 1000)
        chunk_overlap (int): Overlap between chunks (default 0)
        batch_size (int): Number of points to upload per batch (default 100)
    """
    print(f"Loading document: {file_path}")
    loader = TextLoader(file_path)
    documents = loader.load()

    print(f"Splitting document into chunks (size: {chunk_size}, overlap: {chunk_overlap})")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(documents)
    print(f"Document split into {len(docs)} chunks")

    print("Generating embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([doc.page_content for doc in docs])

    # Connect to cloud Qdrant instance using environment variables or fallback to hardcoded values
    qdrant_url = os.getenv("QDRANT_URL", "https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.cNySe9pbHewVBDaZXEUTGhpyWadhc3kWG5LWDTh51r0")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )

    # Check if collection exists, create if it doesn't
    collections = client.get_collections().collections
    collection_names = [col.name for col in collections]

    if collection_name not in collection_names:
        print(f"Creating collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
    else:
        print(f"Collection {collection_name} already exists, adding to existing collection")

    # Prepare points with unique IDs
    print("Preparing points for upload...")
    points = []
    for i, (embedding, doc) in enumerate(zip(embeddings, docs)):
        point = models.PointStruct(
            id=str(uuid.uuid4()),  # Use UUID to avoid ID conflicts
            vector=embedding.tolist(),
            payload={
                "text": doc.page_content,
                "source": getattr(doc, 'metadata', {}).get('source', 'unknown'),
                "chunk_index": i
            },
        )
        points.append(point)

    # Upload in batches to handle large datasets efficiently
    print(f"Uploading {len(points)} points in batches of {batch_size}...")
    total_points = len(points)
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch,
        )
        print(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")

    print(f"Successfully uploaded {total_points} points to collection '{collection_name}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data into Qdrant.")
    parser.add_argument("--file-path", type=str, required=True, help="The path to the text file.")
    parser.add_argument(
        "--collection-name",
        type=str,
        default="rag_chatbot",
        help="The name of the Qdrant collection.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Size of text chunks (default: 1000)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=0,
        help="Overlap between chunks (default: 0)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of points per batch (default: 100)",
    )
    args = parser.parse_args()

    ingest_data(
        args.file_path,
        args.collection_name,
        args.chunk_size,
        args.chunk_overlap,
        args.batch_size
    )
