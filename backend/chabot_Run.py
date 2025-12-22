from cohere import Cohere
from qdrant_client import QdrantClient

COHERE_API_KEY = "UVa38oaEfPZl4EsgLgvWDNqGxP2vj4LF1F6npqwF"
COLLECTION_NAME = "test_ingestion"

co = Cohere(api_key=COHERE_API_KEY)
qdrant = QdrantClient(url="http://localhost:6333")

print("=== Chatbot Ready! Type 'exit' to quit ===")

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    query_vector = co.embed(
        model="embed-english-v2.0",
        texts=[query]
    ).embeddings[0]

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=1,
        with_payload=True
    )

    if results.points:
        print("Chatbot:", results.points[0].payload.get("content", "No content found"))
    else:
        print("Chatbot: Sorry, I don't have an answer for that.")
