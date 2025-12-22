@echo off
REM Script to start both backend and frontend in development mode

echo Starting Backend and Frontend services...
echo ===========================================

REM Start backend in a separate window
start "Backend" cmd /k "cd backend && run_dev.bat"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a separate window
start "Frontend" cmd /k "cd frontend && npm start"

echo Both services started in separate windows.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause