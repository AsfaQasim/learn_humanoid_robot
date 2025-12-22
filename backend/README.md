# Backend - RAG Chatbot API

This directory contains the FastAPI backend for the RAG Chatbot.

## Setup

1.  **Install dependencies**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

    Alternatively, if you use uv:
    ```bash
    cd backend
    uv pip install -r requirements.txt
    ```

    **Note**: If you encounter issues with psycopg2-binary installation, see [DB_INSTALLATION.md](DB_INSTALLATION.md) for alternative installation methods.

2.  **Set up environment variables**:
    Create a `.env` file in the `backend` directory and add the following:
    ```
    GEMINI_API_KEY=your_gemini_api_key
    QDRANT_HOST=your_qdrant_host
    QDRANT_API_KEY=your_qdrant_api_key
    NEON_DATABASE_URL=your_neon_database_url
    ```

## Running the Application

```bash
cd backend
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints

-   `POST /chat`: Send a message to the chatbot.
-   `POST /feedback`: Submit feedback for a chatbot response.

## Data Ingestion

To ingest book content into the Qdrant vector store:

```bash
cd backend
python scripts/ingest_data.py --file-path /path/to/your/book.txt --collection-name your_collection_name
```
