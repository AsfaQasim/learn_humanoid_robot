#!/bin/bash
# Development script to run the RAG Chatbot Backend application with auto-reload
echo "Starting RAG Chatbot Backend application in development mode..."
echo "==============================================================="

# Change to the backend directory
cd "$(dirname "$0")"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the application with auto-reload..."
    PYTHONPATH=. uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "uv not found, using standard Python with auto-reload..."
    PYTHONPATH=. python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
fi