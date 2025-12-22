from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import chat, feedback
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Self-origin
        "http://127.0.0.1:8000"
    ],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(chat.router)
app.include_router(feedback.router)

# Serve static files (built frontend)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve frontend files - only if static directory exists
if os.path.exists(static_dir):
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Skip API routes - they should be handled by the routers
        if full_path in ["chat", "feedback"] or full_path.startswith("chat/") or full_path.startswith("feedback/"):
            from fastapi.responses import JSONResponse
            return JSONResponse({"detail": "API endpoint not found"}, status_code=404)

        # Serve static files if they exist
        static_file_path = os.path.join(static_dir, full_path)
        if os.path.exists(static_file_path):
            from fastapi.responses import FileResponse
            return FileResponse(static_file_path)

        # For all other routes, serve the main index.html (for SPA routing)
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            from fastapi.responses import FileResponse
            return FileResponse(index_path)

        # If no static files exist, return the API root
        return {"Hello": "World"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
