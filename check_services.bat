@echo off
chcp 65001 >nul
echo ========================================
echo Service Status Check
echo ========================================
echo.

echo Checking Backend Service (Port 8000)...
netstat -an | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [✓] Backend service is running on port 8000
    echo     Health check: http://localhost:8000/health
    echo     API docs: http://localhost:8000/docs
) else (
    echo [✗] Backend service is not running on port 8000
)

echo.
echo Checking Frontend Service (Port 3000)...
netstat -an | findstr ":3000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [✓] Frontend service is running on port 3000
    echo     Frontend: http://localhost:3000
) else (
    echo [✗] Frontend service is not running on port 3000
)

echo.
echo ========================================
echo Status check completed
echo ========================================
pause 