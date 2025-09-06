@echo off
chcp 65001 >nul
echo ========================================
echo 重启前后端服务
echo ========================================

echo 正在停止现有服务...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
timeout /t 2 >nul

echo 启动后端服务...
start "Backend" cmd /k "cd backend-python && py main_simple.py"

echo 等待后端启动...
timeout /t 5 >nul

echo 启动前端服务...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo 等待前端启动...
timeout /t 5 >nul

echo ========================================
echo 服务启动完成！
echo 后端: http://localhost:8000
echo 前端: http://localhost:3000
echo ========================================

pause 