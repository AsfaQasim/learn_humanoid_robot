@echo off
REM Script to build frontend and serve with backend in production mode

echo Building and Serving Production Application...
echo =============================================

REM Build the frontend
cd frontend
echo Building frontend...
npm run build
if %errorlevel% neq 0 (
    echo Frontend build failed!
    pause
    exit /b 1
)

echo Frontend build completed successfully!

REM Move the built frontend to backend static directory
cd ..
if not exist "backend\static" mkdir backend\static
xcopy /E /I /Y frontend\build backend\static\

REM Start backend with production settings
cd backend
echo Starting backend in production mode...
start "Backend-Prod" cmd /k "run_app.bat"

echo Production build completed and backend started!
echo Frontend is built and available at http://localhost:8000
pause