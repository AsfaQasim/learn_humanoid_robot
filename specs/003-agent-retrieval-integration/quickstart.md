# Quickstart: RAG Chatbot – Spec 3: Agent creation with retrieval integration

## Overview
Quickstart guide for setting up and running the AI Agent that integrates Qdrant-based retrieval to answer questions grounded in the book's content.

## Prerequisites

### Environment Setup
1. Python 3.11 or higher installed
2. OpenAI API key
3. Qdrant Cloud account and API key
4. Cohere API key
5. Git for version control

### Required Dependencies
The following dependencies are needed for the agent:
- openai>=1.0.0
- qdrant-client
- cohere
- python-dotenv

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install openai qdrant-client cohere python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

### 5. Verify Qdrant Connection
Ensure that your Qdrant collection "document_embeddings" exists and contains the ingested book content from previous specs.

## Running the Agent

### 1. Execute the Agent
Run the agent using the main file:

```bash
python agent.py
```

### 2. Interactive Mode
The agent will start in interactive mode where you can ask questions:

```bash
$ python agent.py
Initializing RAG Agent...
Agent ready! Ask your questions (type 'quit' to exit):
> What are the fundamental principles of robotics?
```

### 3. Programmatic Usage
You can also use the agent programmatically:

```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Ask a question
response = agent.query("What are the fundamental principles of robotics?")
print(response)
```

## Example Usage

### Basic Query
```python
from agent import RAGAgent

agent = RAGAgent()
response = agent.query("What are the fundamental principles of robotics?")
print(response)
```

### Query with Custom Parameters
```python
# Specify number of chunks to retrieve
response = agent.query("What are the fundamental principles of robotics?", top_k=3)
print(response)
```

## Configuration Options

### Environment Variables
- `OPENAI_API_KEY`: API key for OpenAI services
- `QDRANT_URL`: URL for Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant access
- `COHERE_API_KEY`: API key for Cohere embedding services
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: "document_embeddings")
- `AGENT_MODEL`: OpenAI model to use (default: "gpt-4-turbo")

### Agent Parameters
- `top_k`: Number of chunks to retrieve from Qdrant (default: 5)
- `score_threshold`: Minimum relevance score for retrieved chunks (default: 0.3)
- `max_tokens`: Maximum tokens for agent response (default: 1000)

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are set in the `.env` file
2. **Qdrant Connection**: Verify Qdrant URL and API key are correct
3. **No Results**: Check that the Qdrant collection contains ingested content
4. **Rate Limits**: Implement retry logic if encountering API rate limits

### Verification Steps
1. Test Qdrant connection independently
2. Verify embedding models are accessible
3. Confirm OpenAI API is working
4. Check that document embeddings exist in Qdrant

## Development

### Running Tests
```bash
pytest tests/test_agent.py
```

### Code Structure
- `agent.py`: Main agent implementation
- `retrieve.py`: Existing retrieval functionality
- `retriever.py`: Qdrant integration
- `config.py`: Configuration management

## Next Steps

1. Integrate the agent with your application
2. Add monitoring and logging
3. Implement caching for frequently asked questions
4. Add support for conversation history (future enhancement)