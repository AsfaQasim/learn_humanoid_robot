@echo off
echo Starting Backend Server in Production Mode...
echo =============================================
echo Make sure you have set your environment variables:
echo - QDRANT_URL
echo - QDRANT_API_KEY  
echo - COHERE_API_KEY
echo.
echo Starting FastAPI server on http://localhost:8000...
python -c "from app import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"
pause