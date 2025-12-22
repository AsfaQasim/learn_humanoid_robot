import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

def get_qdrant_client():
    """
    Create and return a configured Qdrant client
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_url and qdrant_api_key:
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
    else:
        # Fallback to hardcoded values if environment variables are not set
        client = QdrantClient(
            url="https://2e1ddb8b-10be-4100-8241-514227393167.europe-west3-0.gcp.cloud.qdrant.io:6333",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.cNySe9pbHewVBDaZXEUTGhpyWadhc3kWG5LWDTh51r0",
        )

    return client

# Get client instance
qdrant_client = get_qdrant_client()

# Only print collections in development/testing, not in production
if __name__ == "__main__":
    print(qdrant_client.get_collections())