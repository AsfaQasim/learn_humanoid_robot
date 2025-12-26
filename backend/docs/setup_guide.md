# Setup Guide: Documentation Ingestion Pipeline

## Prerequisites

- Python 3.11+
- uv package manager
- Access to Cohere API
- Access to Qdrant Cloud

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies using uv**
   ```bash
   uv pip install -r requirements.txt
   # Or if using pyproject.toml:
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env to add your API keys
   nano .env
   ```

## Configuration

The pipeline can be configured using environment variables:

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `CHUNK_SIZE`: Size of text chunks (default: 512)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `RATE_LIMIT_DELAY`: Delay between API calls in seconds (default: 1.0)

## Architecture Overview

The ingestion pipeline consists of four main components:

1. **Scraper**: Extracts clean text content from documentation URLs
2. **Chunker**: Divides text into appropriately sized chunks with overlap
3. **Embeddings**: Generates vector representations using Cohere API
4. **Storage**: Stores vectors in Qdrant with metadata

## Running the Pipeline

To run the ingestion pipeline with default settings:

```bash
python main.py
```

To run the pipeline with specific URLs:

```bash
python main.py https://example.com/docs/page1 https://example.com/docs/page2
```

To run the pipeline with custom chunk size and overlap:

```bash
python main.py --chunk-size 1024 --chunk-overlap 100 https://example.com/docs
```

To run with verbose logging:

```bash
python main.py --verbose https://example.com/docs
```

## Running Tests

To run the complete test suite:

```bash
python -m pytest tests/
```

To run specific test files:

```bash
python -m pytest tests/test_scraper.py
python -m pytest tests/test_chunker.py
python -m pytest tests/test_embeddings.py
python -m pytest tests/test_storage.py
python -m pytest tests/test_integration.py
```

To run tests with verbose output:

```bash
python -m pytest tests/ -v
```

## Pipeline Performance

The pipeline is optimized to process 1000 text chunks within 30 minutes. For larger volumes, consider:

- Adjusting the `RATE_LIMIT_DELAY` to balance speed and API limits
- Using appropriate `CHUNK_SIZE` to balance context and processing efficiency
- Monitoring API usage to stay within Cohere and Qdrant limits

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure `COHERE_API_KEY` and `QDRANT_URL` are properly set in `.env`
2. **Rate Limiting**: Adjust `RATE_LIMIT_DELAY` in `.env` if encountering rate limit errors
3. **Network Issues**: Check internet connectivity and URL accessibility

### Logging

The pipeline logs information to both console and log files. Use `--verbose` flag for detailed logging.

## Development

### Adding New Features

The codebase follows a modular architecture:
- Add new scraping logic to `src/scraper.py`
- Add new chunking strategies to `src/chunker.py`
- Add new embedding models to `src/embeddings.py`
- Add new storage backends to `src/storage.py`

### Testing Strategy

The test suite includes:
- Unit tests for individual components
- Integration tests for complete pipeline
- Performance tests for large volumes
- Edge case tests for error conditions