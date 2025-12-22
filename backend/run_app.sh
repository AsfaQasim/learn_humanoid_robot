#!/bin/bash
# Shell script to run the RAG Chatbot Backend application

echo "Starting RAG Chatbot Backend application..."
echo "============================================="

# Change to the backend directory
cd "$(dirname "$0")"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the application..."
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
else
    echo "uv not found, using standard Python..."
    python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000
fi