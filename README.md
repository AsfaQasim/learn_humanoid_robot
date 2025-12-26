# RAG Chatbot System for Physical AI & Humanoid Robotics

This is a comprehensive RAG (Retrieval-Augmented Generation) chatbot system that uses content from the Physical AI & Humanoid Robotics textbook available at https://learn-humanoid-robot.vercel.app/, featuring a FastAPI backend with Google Gemini integration and Qdrant vector database, along with a modern web frontend and terminal interface.

## Architecture

The system is built in 3 parts:

### Part 1: FastAPI Backend for Ingestion
- Document ingestion via file upload (PDF, text) or direct text input
- Text chunking with configurable size and overlap
- Vector storage using Qdrant Cloud
- Embedding generation using Google Gemini
- REST API endpoints for ingestion and querying

### Part 2: Gemini Integration for Terminal Querying
- Terminal-based interface for querying the backend
- Support for both full document retrieval and selected text context
- Interactive command-line interface

### Part 3: Frontend UI Implementation
- Modern web interface with chat functionality
- File upload and text ingestion capabilities
- Real-time chat interface
- Responsive design

## Project Structure

- **Backend**: FastAPI application in the `backend/` directory
- **Frontend**: Docusaurus site in the `frontend/` directory (existing)
- **Chat Integration**: React-based chat components in `frontend/src/components/` (existing)
- **New RAG Backend**: FastAPI RAG service in `backend/src/`
- **Static Frontend**: HTML/CSS/JS interface in `backend/static/`

## Setup Instructions

### Prerequisites
- Python 3.10+
- Google Cloud account with Gemini API access
- Qdrant Cloud account (or local Qdrant instance)

### Environment Variables
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_google_gemini_api_key
QDRANT_URL=your_qdrant_cloud_url (e.g., https://your-cluster.us-east4.gcp.cloud.qdrant.io)
QDRANT_API_KEY=your_qdrant_api_key
```

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python run_app.py
```
Or using uvicorn directly:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Options
You have two frontend options:

**Option 1: New RAG UI** (Recommended for RAG functionality)
- Access at `http://localhost:8000` after starting the backend
- Modern interface with ingestion and chat capabilities

**Option 2: Existing Docusaurus Frontend** (Maintains existing textbook functionality)
- Start both services with the combined script:
   ```bash
   start_both.bat
   ```
- Backend available at `http://localhost:8000`
- Frontend available at `http://localhost:3000`

### Terminal Interface
Run the terminal interface:
```bash
python backend/terminal_query.py
```

## API Endpoints

### POST `/ingest`
Ingest documents into the vector store.

Parameters:
- `file`: PDF or text file to upload (optional)
- `text`: Direct text input (optional, but either file or text must be provided)
- `chunk_size`: Size of text chunks (default: 1000)
- `overlap`: Overlap between chunks (default: 100)

### POST `/query`
Query the RAG system.

Parameters:
- `question`: The question to ask
- `selected_text`: Optional text to use as context instead of retrieving from vector store

### GET `/health`
Health check endpoint.

## Usage Examples

### Using the New Web Interface
1. Start the backend server
2. Open `http://localhost:8000` in your browser
3. Use the left panel to ingest documents
4. Use the chat interface to ask questions

### Using the Terminal Interface
1. Start the backend server
2. Run `python backend/terminal_query.py`
3. Type questions directly, or use format `question|selected text` to provide context

### Direct API Usage
```bash
# Ingest text
curl -X POST -F "text=Your document content here" http://localhost:8000/ingest

# Query the system
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is AI?", "selected_text": null}' \
  http://localhost:8000/query
```

## Testing
Run the comprehensive test suite:
```bash
python backend/test_complete_system.py
```

## Running Both Systems
To run both the existing textbook frontend and the new RAG backend:

1. **Development Mode**:
   ```bash
   start_both.bat
   ```
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

2. **Production Mode**:
   ```bash
   build_and_serve_prod.bat
   ```
   - Application served from: `http://localhost:8000`

## Deployment
- Backend: Deploy to platforms like Render, Heroku, or AWS
- Qdrant: Use Qdrant Cloud or self-hosted instance
- Frontend: The new UI is served by the backend, so deployment is unified

## Technologies Used
- Python 3.10+
- FastAPI
- Google Generative AI (Gemini)
- Qdrant Vector Database
- PyPDF2
- Uvicorn
- HTML/CSS/JavaScript (for frontend)

## New RAG Chatbot System for test_ingestion_custom Collection

Added specialized RAG chatbot system that works with your existing `test_ingestion_custom` collection:

### Features:
- Qdrant Data Retrieval: Performs vector similarity search on `test_ingestion_custom` collection
- Top-k Retrieval: Fetches top 3 most relevant documents for each query
- Context-Aware Answers: Generates precise answers based on retrieved documents
- Two Interface Options: FastAPI endpoint and terminal interface
- Production Ready: Secure handling of API keys via environment variables

### New Components:
- **Custom RAG Service**: `backend/src/services/custom_rag_service.py`
- **Ask Endpoint**: `backend/ask_endpoint.py` (runs on port 8001)
- **Terminal Interface**: `backend/terminal_chatbot.py`
- **Test Script**: `backend/test_rag_system.py`

### Setup:
1. Ensure your Qdrant collection `test_ingestion_custom` exists with book data
2. Update your `.env` with API keys:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

### Usage:
- **FastAPI Endpoint**: `python backend/ask_endpoint.py` → `http://localhost:8001/ask`
- **Terminal Interface**: `python backend/terminal_chatbot.py`
- **Test System**: `python backend/test_rag_system.py`

## Features

- Interactive textbook content with Docusaurus documentation framework
- AI-powered RAG chatbot for answering questions about robotics and AI
- Source citation and feedback system for chat responses
- Document ingestion and retrieval capabilities
- Modern web interface with chat functionality
- Terminal-based querying interface
- Responsive design for all device sizes
- Specialized RAG system for Physical AI & Humanoid Robotics content from https://learn-humanoid-robot.vercel.app/
- Automated content ingestion from the target website
- Question answering system specifically trained on robotics and AI content

## Usage for Physical AI & Humanoid Robotics Content

### 1. Ingest Website Content

First, ingest the content from the Physical AI & Humanoid Robotics website:

```bash
python ingest_robotics_content.py
```

### 2. Ask Questions

Once the content is ingested, you can ask questions about Physical AI & Humanoid Robotics:

Interactive Mode:
```bash
python robotics_qa.py --interactive
```

Single Question:
```bash
python robotics_qa.py "What is physical AI?"
```

### 3. Validate the System

To validate that the retrieval pipeline is working correctly:

```bash
python robotics_qa.py --validate
```
