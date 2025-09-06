@echo off
echo ========================================
echo 骨质疏松症随访系统 - 状态检查
echo ========================================
echo.

:: 检查后端服务状态
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [✓] 后端服务运行中 (端口8000)
    echo     地址: http://localhost:8000
    echo     API文档: http://localhost:8000/docs
) else (
    echo [✗] 后端服务未运行 (端口8000)
)

echo.

:: 检查前端服务状态
netstat -an | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo [✓] 前端服务运行中 (端口3000)
    echo     地址: http://localhost:3000
) else (
    echo [✗] 前端服务未运行 (端口3000)
)

echo.

:: 检查Python环境
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%a in ('python --version 2^>^&1') do (
        echo [✓] Python环境: %%a
    )
) else (
    echo [✗] Python环境未安装或未配置
)

:: 检查Node.js环境
node --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=1" %%a in ('node --version 2^>^&1') do (
        echo [✓] Node.js环境: %%a
    )
) else (
    echo [✗] Node.js环境未安装或未配置
)

echo.
echo ========================================
echo 状态检查完成
echo ========================================
pause 