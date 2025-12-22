@echo off
REM Batch script to run the RAG Chatbot Backend application

echo Starting RAG Chatbot Backend application...
echo =============================================

REM Change to the backend directory
cd /d "%~dp0"

REM Check if uv is available
where uv >nul 2>nul
if %errorlevel% == 0 (
    echo Using uv to run the application...
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
) else (
    echo uv not found, using standard Python...
    python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
)

pause