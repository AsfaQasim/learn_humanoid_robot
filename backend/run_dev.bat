@echo off
echo Starting Backend Server...
echo ============================
echo Make sure you have set your environment variables:
echo - QDRANT_URL
echo - QDRANT_API_KEY  
echo - COHERE_API_KEY
echo.
echo Starting FastAPI server on http://localhost:8000...
python run_server.py
pause