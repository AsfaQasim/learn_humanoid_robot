@echo off
echo Running Startup Verification for RAG Chatbot Application
echo =================================================================

echo.
echo 1. Checking if backend is running on port 8000...
tasklist | find /i "python.exe" | find /i "run_server.py" >nul
if %errorlevel% == 0 (
    echo    ✓ Backend appears to be running
) else (
    echo    ⚠ Backend may not be running
    echo    To start backend: cd backend && python run_server.py
)

echo.
echo 2. Checking if frontend is running on port 3000...
tasklist | find /i "node.exe" | find /i "docusaurus" >nul
if %errorlevel% == 0 (
    echo    ✓ Frontend appears to be running
) else (
    echo    ⚠ Frontend may not be running
    echo    To start frontend: cd frontend && npm start
)

echo.
echo 3. Checking for required environment files...
if exist "backend\.env" (
    echo    ✓ Backend .env file exists
) else (
    echo    ⚠ Backend .env file not found
    echo    Create from example: copy backend\.env.example backend\.env
)

if exist "frontend\.env.local" (
    echo    ✓ Frontend .env.local file exists
) else (
    echo    ⚠ Frontend .env.local file not found (optional for development)
)

echo.
echo 4. Checking for required dependencies...
cd backend
python -c "import fastapi, uvicorn, requests, cohere, qdrant_client" >nul 2>&1
if %errorlevel% == 0 (
    echo    ✓ Backend Python dependencies are available
) else (
    echo    ⚠ Backend Python dependencies may be missing
    echo    Install with: pip install -r requirements.txt
)

cd ..\frontend
if exist "node_modules" (
    echo    ✓ Frontend node_modules directory exists
) else (
    echo    ⚠ Frontend dependencies may need to be installed
    echo    Run: npm install
)

echo.
echo 5. Testing backend connectivity...
cd ..\backend
python -c "import requests; print('Backend connectivity: OK') if requests.get('http://localhost:8000/health', timeout=5).status_code == 200 else print('Backend connectivity: FAILED')" >nul 2>&1
if %errorlevel% == 0 (
    echo    ✓ Backend connectivity test completed (may show result in separate window)
) else (
    echo    ⚠ Backend connectivity test failed or backend not running
)

echo.
echo 6. Displaying current configuration...
echo    Backend URL: http://localhost:8000
echo    Frontend URL: http://localhost:3000
echo    Chat endpoint: http://localhost:8000/chat

echo.
echo =================================================================
echo VERIFICATION COMPLETE
echo.
echo TO START THE APPLICATION:
echo   1. Backend: cd backend && python run_server.py
echo   2. Frontend: cd frontend && npm start
echo.
echo TO RUN COMPREHENSIVE TESTS:
echo   cd backend && python comprehensive_test.py
echo.
pause