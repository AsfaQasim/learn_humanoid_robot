import uvicorn
import sys
import os

if __name__ == "__main__":
    # Add the parent directory to the path so we can import modules
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    # Run the FastAPI server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )