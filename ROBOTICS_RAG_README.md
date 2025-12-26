# Physical AI & Humanoid Robotics RAG System

This project implements a RAG (Retrieval-Augmented Generation) based question answering system that uses content from the Physical AI & Humanoid Robotics textbook available at [https://learn-humanoid-robot.vercel.app/](https://learn-humanoid-robot.vercel.app/).

## Overview

The system consists of:
1. An ingestion pipeline that scrapes content from the target website
2. A vector database (Qdrant) for storing embeddings
3. A retrieval system that finds relevant content based on user queries
4. An AI agent that generates answers grounded in the retrieved content

## Prerequisites

Before running the system, you need to set up your API keys in the `.env` file:

```bash
# .env file should contain:
COHERE_API_KEY=your-cohere-api-key-here
QDRANT_URL=your-qdrant-url-here
QDRANT_API_KEY=your-qdrant-api-key-here
Gemini_Api_Key=your-gemini-api-key-here
```

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Update your `.env` file with your actual API keys

## Usage

### 1. Ingest Website Content

First, ingest the content from the Physical AI & Humanoid Robotics website:

```bash
python ingest_robotics_content.py
```

This will:
- Discover and scrape all pages from the website
- Chunk the content appropriately
- Generate embeddings using Cohere
- Store the embeddings in Qdrant for retrieval

### 2. Ask Questions

Once the content is ingested, you can ask questions about Physical AI & Humanoid Robotics:

#### Interactive Mode
```bash
python robotics_qa.py --interactive
```

#### Single Question
```bash
python robotics_qa.py "What is physical AI?"
```

#### With Custom Parameters
```bash
python robotics_qa.py --top-k 7 --interactive
```

### 3. Validate the System

To validate that the retrieval pipeline is working correctly:

```bash
python robotics_qa.py --validate
```

## System Components

- `ingest_robotics_content.py`: Script to scrape and ingest content from the target website
- `robotics_qa.py`: Main interface for asking questions about the content
- `agent.py`: AI agent that uses OpenAI Agents SDK with Qdrant retrieval
- `retriever.py`: Core retrieval logic for finding relevant content
- `backend/main.py`: Main ingestion pipeline
- `backend/src/`: Core backend components (scraper, chunker, embeddings, storage)

## How It Works

1. **Ingestion**: The system scrapes content from the Physical AI & Humanoid Robotics website, chunks it into manageable pieces, and generates embeddings using Cohere's embedding model.

2. **Storage**: The embeddings are stored in a Qdrant vector database with metadata for efficient retrieval.

3. **Retrieval**: When a user asks a question, the system generates an embedding for the question and performs a semantic search in the vector database to find the most relevant content chunks.

4. **Generation**: The AI agent uses the retrieved content to generate an answer that is grounded in the source material.

## Example Questions

You can ask questions like:
- "What are the main components of a humanoid robot?"
- "Explain the principles of physical AI"
- "What are the applications of humanoid robots in real-world scenarios?"
- "How do humanoid robots perceive their environment?"
- "What is the difference between traditional robotics and physical AI?"

## Troubleshooting

If you encounter issues:
1. Verify your API keys are correct in the `.env` file
2. Check that your Qdrant instance is accessible
3. Run validation to check the retrieval pipeline: `python robotics_qa.py --validate`
4. Make sure the content has been properly ingested before asking questions

## Architecture

The system uses:
- **Cohere** for text embeddings
- **Qdrant** for vector storage and similarity search
- **Gemini** for answer generation
- **BeautifulSoup** for web scraping
- **OpenAI Agents SDK** for agent functionality