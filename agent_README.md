# RAG Chatbot Agent with Qdrant Retrieval Integration

This project implements an AI Agent that integrates Qdrant-based retrieval to answer questions grounded in book content using the OpenAI Agents SDK.

## Features

- **OpenAI Agent SDK Integration**: Uses the official OpenAI Agents SDK to create intelligent agents
- **Qdrant Retrieval**: Integrates with Qdrant vector database for semantic search
- **Grounded Responses**: Ensures responses are based on retrieved document chunks
- **Error Handling**: Comprehensive error handling for API failures and connection issues
- **Query Validation**: Validates queries for security and quality
- **Performance Optimized**: Includes timeout handling and retry mechanisms

## Requirements

- Python 3.11+
- OpenAI API key
- Qdrant Cloud account and API key
- Cohere API key

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables in a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

## Usage

### Command Line Interface

Run the agent from the command line:

```bash
# Single query mode
python agent.py "What are the fundamental principles of robotics?"

# Interactive mode
python agent.py --interactive

# With custom parameters
python agent.py --top-k 3 "Explain machine learning algorithms"

# With verbose logging
python agent.py --verbose "Your query here"
```

### Programmatic Usage

```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Query the agent
response = agent.query("What are the fundamental principles of robotics?", top_k=5)

# Access the response
print(response['response'])
print(f"Retrieved {response['retrieval_count']} chunks")
print(response['retrieved_chunks'])

# Clean up when done
agent.close()
```

## Architecture

The system consists of:

1. **RAGAgent**: Main agent class that orchestrates the entire process
2. **Qdrant Integration**: Uses existing retriever functionality to search vector database
3. **OpenAI Agent SDK**: Uses the official OpenAI Agents SDK with function tools for processing queries with retrieved context
4. **Validation Layer**: Ensures queries and responses meet quality standards
5. **Error Handling**: Comprehensive error handling and retry mechanisms

## Error Handling

The agent includes several error handling mechanisms:

- **Connection Failures**: Graceful handling of Qdrant connection issues with retry logic
- **Query Validation**: Validates queries for length, special characters, and injection attempts
- **Timeout Handling**: 60-second timeout for assistant responses
- **Retry Mechanisms**: Exponential backoff for failed retrieval attempts
- **Logging**: Comprehensive logging for troubleshooting

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest test_agent.py -v

# Run performance tests
python -m pytest test_agent_performance.py -v
```

## Configuration

The agent can be configured via environment variables in the `.env` file:

- `OPENAI_API_KEY`: OpenAI API key
- `QDRANT_URL`: Qdrant Cloud URL
- `QDRANT_API_KEY`: Qdrant API key
- `COHERE_API_KEY`: Cohere API key
- `CHUNK_SIZE`: Size of text chunks (default: 512)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `RATE_LIMIT_DELAY`: Delay between API calls (default: 1.0)

## Security

- Query validation prevents SQL injection and script injection attempts
- Proper error handling prevents information disclosure
- API keys are loaded from environment variables
- Input sanitization for all user queries

## Performance

- Response time optimized to stay under 2 seconds
- Timeout handling prevents hanging requests
- Efficient retrieval with configurable top-k values
- Connection pooling and reuse where possible

## Limitations

- Requires valid API keys for OpenAI, Qdrant, and Cohere
- Responses depend on quality and coverage of ingested documents
- Rate limits apply based on your API provider plans
- Complex queries may take longer to process