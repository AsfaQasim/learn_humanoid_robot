@echo off
echo Installing Backend Dependencies...
echo ================================

REM Navigate to backend directory
cd backend

REM Install Python dependencies
pip install -r requirements.txt

REM Navigate back to project root
cd ..

REM Navigate to frontend directory
cd frontend

REM Install Node.js dependencies
npm install

REM Navigate back to project root
cd ..

echo.
echo Installation complete!
echo.
echo To start the application:
echo   1. Make sure you have set your environment variables
echo   2. Run: start_both.bat
echo.
pause