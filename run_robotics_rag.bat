@echo off
REM Script to run the complete Physical AI & Humanoid Robotics RAG system workflow

echo ================================================
echo Physical AI & Humanoid Robotics RAG System
echo ================================================
echo.

:menu
echo Select an option:
echo 1. Ingest website content (one-time setup)
echo 2. Ask questions interactively
echo 3. Run a test query
echo 4. Validate the system
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto ingest
if "%choice%"=="2" goto interactive
if "%choice%"=="3" goto test
if "%choice%"=="4" goto validate
if "%choice%"=="5" goto exit

echo Invalid choice. Please try again.
echo.
goto menu

:ingest
echo.
echo Starting content ingestion from https://learn-humanoid-robot.vercel.app/...
python ingest_robotics_content.py
pause
goto menu

:interactive
echo.
echo Starting interactive Q&A session...
python robotics_qa.py --interactive
pause
goto menu

:test
echo.
echo Running test query...
python robotics_qa.py --test-query
pause
goto menu

:validate
echo.
echo Validating the retrieval pipeline...
python robotics_qa.py --validate
pause
goto menu

:exit
echo.
echo Thank you for using the Physical AI & Humanoid Robotics RAG system!
exit /b