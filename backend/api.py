"""
Vercel serverless function entry point for the FastAPI application
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main app from app.py
from app import app

# Add CORS middleware for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        os.getenv("FRONTEND_URL", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Export the FastAPI app instance as the handler
handler = app

# For Vercel Python runtime
# The handler is the ASGI application that Vercel will call
application = app