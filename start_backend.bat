@echo off
chcp 65001 >nul
echo ========================================
echo Osteoporosis Follow-up System - Backend
echo ========================================
echo.

:: Set working directory
cd /d "%~dp0backend-python"
echo Current directory: %CD%
echo.

:: Check Python installation
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please ensure Python is installed
    pause
    exit /b 1
)

:: Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found
    pause
    exit /b 1
)

:: Check if port 8000 is occupied
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo Warning: Port 8000 is occupied, trying to stop existing service...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 3 /nobreak >nul
)

echo Starting backend server...
echo Service URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop server
echo ========================================

:: Start backend service
py main.py

echo.
echo Backend service stopped
pause 