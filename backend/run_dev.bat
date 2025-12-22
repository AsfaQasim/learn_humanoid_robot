@echo off
REM Development batch script to run the RAG Chatbot Backend application with auto-reload
echo Starting RAG Chatbot Backend application in development mode...
echo ===============================================================

REM Change to the backend directory
cd /d "%~dp0"

REM Set PYTHONPATH to include current directory
set PYTHONPATH=%~dp0;%PYTHONPATH%

REM Check if uv is available
where uv >nul 2>nul
if %errorlevel% == 0 (
    echo Using uv to run the application with auto-reload...
    uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo uv not found, using standard Python with auto-reload...
    python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
)

pause