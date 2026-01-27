@echo off
echo Setting up Physical AI & Humanoid Robotics Application
echo =====================================================

REM Check if backend is running
echo Checking if backend is running on port 8000...
netstat -an | find "8000" >nul
if errorlevel 1 (
    echo Backend not detected on port 8000. Starting backend...
    start "Backend" cmd /k "cd backend && python run_server.py"
    echo Waiting for backend to start...
    timeout /t 10 /nobreak >nul
) else (
    echo Backend is already running on port 8000
)

REM Check if frontend is running
echo Checking if frontend is running on port 3000...
netstat -an | find "3000" >nul
if errorlevel 1 (
    echo Frontend not detected on port 3000. Starting frontend...
    start "Frontend" cmd /k "cd frontend && npm start"
) else (
    echo Frontend is already running on port 3000
)

echo.
echo Application setup complete!
echo - Backend should be available at http://localhost:8000
echo - Frontend should be available at http://localhost:3000
echo.
echo You can test the backend API by running:
echo   cd backend && python test_api.py
echo.
pause