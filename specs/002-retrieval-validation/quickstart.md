# Quickstart: RAG Data Retrieval and Pipeline Validation

## Setup

1. **Prerequisites**
   - Python 3.11+
   - Access to Cohere API
   - Access to Qdrant Cloud with stored embeddings

2. **Environment Configuration**
   ```bash
   # Copy the example environment file
   cp backend/.env.example .env
   # Edit .env to add your API keys
   nano .env
   ```

3. **Install Dependencies**
   ```bash
   pip install qdrant-client cohere python-dotenv
   ```

## Running the Retrieval System

1. **Basic Retrieval**
   ```bash
   python retrieve.py "What are robotics fundamentals?"
   ```

2. **With Custom Top-K Value**
   ```bash
   python retrieve.py --query "What are robotics fundamentals?" --top-k 10
   ```

3. **With Filters**
   ```bash
   python retrieve.py --query "What are robotics fundamentals?" --filter-url "https://example.com/docs/robotics"
   ```

## Validation

1. **Run Pipeline Validation**
   ```bash
   python retrieve.py --validate --queries "What are robotics fundamentals?,How do I implement a controller?"
   ```

2. **Check Retrieval Accuracy**
   ```bash
   python retrieve.py --test-query "sample query for accuracy check" --expected-source "expected-document-url"
   ```

## Configuration

The retrieval system uses the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `EMBEDDING_MODEL`: Cohere embedding model to use (default: embed-english-v3.0)
- `TOP_K_DEFAULT`: Default number of results to return (default: 5)
- `SIMILARITY_THRESHOLD`: Minimum similarity threshold (default: 0.7)

## Architecture

The retrieval system consists of:

1. **Query Processor**: Handles incoming queries and generates embeddings
2. **Vector Search**: Performs semantic search against Qdrant
3. **Result Formatter**: Formats and enriches results with metadata
4. **Validator**: Validates retrieval pipeline and embedding compatibility

## Testing

Run validation tests:
```bash
python -m pytest tests/test_retrieval.py
```