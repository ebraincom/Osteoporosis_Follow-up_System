@echo off
chcp 65001 >nul
echo ========================================
echo Osteoporosis Follow-up System - Start All
echo ========================================
echo.

:: Check if backend service is running
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo Backend service is running (port 8000)
) else (
    echo Starting backend service...
    start "Backend Service" cmd /k "start_backend.bat"
    timeout /t 5 /nobreak >nul
)

:: Check if frontend service is running
netstat -an | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo Frontend service is running (port 3000)
) else (
    echo Starting frontend service...
    start "Frontend Service" cmd /k "start_frontend.bat"
    timeout /t 5 /nobreak >nul
)

echo.
echo ========================================
echo Services started!
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to open frontend page...
echo ========================================
pause

:: Open frontend page
start http://localhost:3000

echo.
echo System is running, please keep command windows open
echo Closing windows will stop the services
pause 