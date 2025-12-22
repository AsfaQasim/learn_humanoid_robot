import uuid
from typing import List, Optional
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv


load_dotenv()

class ChunkManager:
    """
    A utility class to manage document chunking, embedding generation, and Qdrant upload
    with proper batching for large datasets.
    """

    def __init__(self,
                 chunk_size: int = 1000,
                 chunk_overlap: int = 0,
                 batch_size: int = 100,
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.batch_size = batch_size
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.model = SentenceTransformer(embedding_model)

    def chunk_document(self, file_path: str) -> List:
        """Load and chunk a document"""
        loader = TextLoader(file_path)
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def generate_embeddings(self, docs: List) -> List:
        """Generate embeddings for document chunks"""
        return self.model.encode([doc.page_content for doc in docs])

    def create_points(self, docs: List, embeddings: List) -> List:
        """Create Qdrant PointStruct objects from docs and embeddings"""
        points = []
        for i, (embedding, doc) in enumerate(zip(embeddings, docs)):
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "text": doc.page_content,
                    "source": getattr(doc, 'metadata', {}).get('source', 'unknown'),
                    "chunk_index": i
                },
            )
            points.append(point)
        return points

    def upload_in_batches(self, client: QdrantClient, collection_name: str, points: List):
        """Upload points to Qdrant in batches"""
        total_points = len(points)
        print(f"Uploading {total_points} points in batches of {self.batch_size}")

        for i in range(0, len(points), self.batch_size):
            batch = points[i:i + self.batch_size]
            client.upsert(
                collection_name=collection_name,
                points=batch,
            )
            print(f"Uploaded batch {i//self.batch_size + 1}/{(len(points)-1)//self.batch_size + 1}")

        print(f"Successfully uploaded {total_points} points to collection '{collection_name}'")


def ingest_file_in_chunks(
    file_path: str,
    collection_name: str,
    qdrant_client: QdrantClient,
    chunk_size: int = 1000,
    chunk_overlap: int = 0,
    batch_size: int = 100,
    embedding_model: str = "all-MiniLM-L6-v2"
):
    """
    Main function to ingest a file into Qdrant with chunking

    Args:
        file_path: Path to the file to ingest
        collection_name: Name of the Qdrant collection
        qdrant_client: Configured QdrantClient instance
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        batch_size: Number of points to upload per batch
        embedding_model: Name of the sentence transformer model to use
    """
    chunk_manager = ChunkManager(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        batch_size=batch_size,
        embedding_model=embedding_model
    )

    # Load and chunk the document
    print(f"Loading and chunking document: {file_path}")
    docs = chunk_manager.chunk_document(file_path)
    print(f"Created {len(docs)} chunks")

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = chunk_manager.generate_embeddings(docs)

    # Create points
    print("Creating Qdrant points...")
    points = chunk_manager.create_points(docs, embeddings)

    # Ensure collection exists
    collections = qdrant_client.get_collections().collections
    collection_names = [col.name for col in collections]

    if collection_name not in collection_names:
        print(f"Creating collection: {collection_name}")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
    else:
        print(f"Collection {collection_name} already exists, adding to existing collection")

    # Upload in batches
    chunk_manager.upload_in_batches(qdrant_client, collection_name, points)

    print(f"Ingestion complete for collection '{collection_name}'")


def get_qdrant_client() -> QdrantClient:
    """
    Create and return a Qdrant client with proper configuration
    """
    qdrant_url = os.getenv("QDRANT_URL", "https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.cNySe9pbHewVBDaZXEUTGhpyWadhc3kWG5LWDTh51r0")

    return QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )


def create_test_document(file_path: str):
    """
    Create a test document for testing purposes
    """
    test_content = """
    Artificial Intelligence and Machine Learning
    ============================================

    Introduction to AI
    ------------------
    Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.

    Machine Learning
    ----------------
    Machine learning (ML) is the study of computer algorithms that can improve automatically through experience and by the use of data. It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to do so.

    Deep Learning
    -------------
    Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep learning architectures such as deep neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, climate science, material inspection and board game programs.

    Applications of AI
    ------------------
    AI is used in a wide range of applications including:
    - Virtual assistants like Siri and Alexa
    - Recommendation systems on Netflix and Amazon
    - Self-driving cars
    - Medical diagnosis
    - Fraud detection in banking
    - Image and speech recognition
    - Natural language processing

    Future of AI
    ------------
    The future of AI looks promising with advances in areas like:
    - General artificial intelligence
    - Quantum computing integration
    - Ethical AI development
    - AI safety research
    - Human-AI collaboration
    - Automated machine learning (AutoML)
    """

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(test_content)

    print(f"Test document created at: {file_path}")