@echo off
echo ========================================
echo 骨质疏松症随访系统 - 停止所有服务
echo ========================================
echo.

echo 正在停止前端服务 (端口3000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000"') do (
    taskkill /f /pid %%a >nul 2>&1
    echo 已停止进程 PID: %%a
)

echo 正在停止后端服务 (端口8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    taskkill /f /pid %%a >nul 2>&1
    echo 已停止进程 PID: %%a
)

echo.
echo 所有服务已停止
echo ========================================
pause 