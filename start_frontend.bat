@echo off
chcp 65001 >nul
echo ========================================
echo Osteoporosis Follow-up System - Frontend
echo ========================================
echo.

:: Set working directory
cd /d "%~dp0frontend"
echo Current directory: %CD%
echo.

:: Set Node.js path first
set PATH=C:\Program Files\nodejs;%PATH%

:: Check Node.js installation
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found, please ensure Node.js is installed
    echo Install path: C:\Program Files\nodejs
    pause
    exit /b 1
)

:: Check if package.json exists
if not exist "package.json" (
    echo Error: package.json not found
    pause
    exit /b 1
)

:: Check if node_modules exists
if not exist "node_modules" (
    echo Warning: node_modules not found, installing dependencies...
    npm install
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Check if port 3000 is occupied
netstat -an | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo Warning: Port 3000 is occupied, trying to stop existing service...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 3 /nobreak >nul
)

echo Starting frontend server...
echo Service URL: http://localhost:3000
echo Proxy config: /api -> http://localhost:8000
echo.
echo Press Ctrl+C to stop server
echo ========================================

:: Start frontend service
npx vite --host 0.0.0.0 --port 3000

echo.
echo Frontend service stopped
pause 