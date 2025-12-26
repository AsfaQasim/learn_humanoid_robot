# Quickstart: Documentation Ingestion Pipeline

## Setup

1. **Prerequisites**
   - Python 3.11+
   - uv package manager
   - Access to Cohere API
   - Access to Qdrant Cloud

2. **Clone and Setup**
   ```bash
   # Create backend directory
   mkdir backend && cd backend

   # Initialize project with uv
   uv init
   ```

3. **Environment Configuration**
   ```bash
   # Create .env file with your API keys
   cp .env.example .env
   # Edit .env to add COHERE_API_KEY and QDRANT_API_KEY
   ```

4. **Install Dependencies**
   ```bash
   uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv transformers
   ```

## Running the Pipeline

1. **Basic Execution**
   ```bash
   python main.py
   ```

2. **Configuration**
   - Set `COHERE_API_KEY` in environment for embedding generation
   - Set `QDRANT_URL` and `QDRANT_API_KEY` for vector storage
   - Set `DOC_URLS` for the documentation URLs to process

## Architecture

The pipeline consists of 4 main components:
1. **Scraper**: Extracts clean text from documentation URLs
2. **Chunker**: Divides text into appropriately sized chunks with overlap
3. **Embeddings**: Generates vector representations using Cohere
4. **Storage**: Stores vectors in Qdrant with metadata

## Testing

Run tests to verify functionality:
```bash
python -m pytest tests/
```

## Customization

- Adjust chunk size in `src/chunker.py`
- Modify scraping selectors in `src/scraper.py`
- Update embedding model in `src/embeddings.py`