# Quickstart: RAG Chatbot Integration

**Date**: 2025-12-11
**Input**: `specs/2-rag-chatbot-integration/plan.md`

This document provides a quickstart guide for setting up and running the RAG Chatbot.

---

## Prerequisites

- Python 3.11
- Poetry for dependency management
- Docker
- Access to OpenAI, Qdrant, and Neon accounts

---

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies**:
    ```bash
    poetry install
    ```

3.  **Set up environment variables**:
    Create a `.env` file in the `backend` directory and add the following:
    ```
    OPENAI_API_KEY=...
    QDRANT_API_KEY=...
    QDRANT_HOST=...
    NEON_DATABASE_URL=...
    ```

---

## Running the Application

1.  **Start the backend server**:
    ```bash
    cd backend
    poetry run uvicorn src.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

2.  **Start the frontend application**:
    ```bash
    cd frontend
    npm install
    npm start
    ```
    The frontend will be available at `http://localhost:3000`.

---

## Ingesting Data

To ingest the book content into the vector database, run the ingestion script:

```bash
cd backend
poetry run python scripts/ingest_data.py --path /path/to/book/content
```
