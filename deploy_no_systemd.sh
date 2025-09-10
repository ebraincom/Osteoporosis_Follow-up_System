#!/bin/bash

# 骨质疏松症随访系统部署脚本 (无systemd版本)
# 服务器IP: 117.50.198.126

set -e

echo "🚀 开始部署骨质疏松症随访系统到GPU服务器..."
echo "📍 服务器IP: 117.50.198.126"
echo "🖥️  系统配置: Ubuntu 22.04 + CUDA 12.6 + Python 3.12"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，开始安装..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 启动Docker服务 (无systemd版本)
echo "🐳 启动Docker服务..."
if ! docker ps &> /dev/null; then
    echo "Docker未运行，尝试启动..."
    dockerd &
    sleep 10
    
    # 检查Docker是否启动成功
    if ! docker ps &> /dev/null; then
        echo "❌ Docker启动失败，尝试使用service命令..."
        service docker start
        sleep 5
    fi
fi

# 验证Docker运行状态
if docker ps &> /dev/null; then
    echo "✅ Docker服务运行正常"
else
    echo "❌ Docker服务启动失败"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs
mkdir -p nginx/ssl
mkdir -p backend-python/uploads
mkdir -p backend-python/backups
mkdir -p backend-python/models

# 检查环境配置文件
if [ ! -f backend-python/.env ]; then
    echo "📋 创建生产环境配置文件..."
    cat > backend-python/.env << EOF
# 生产环境配置
ENVIRONMENT=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./osteoporosis.db
REDIS_URL=redis://redis:6379/0

# CORS设置
ALLOWED_HOSTS=["*"]

# JWT设置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 日志级别
LOG_LEVEL=INFO

# 文件上传设置
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

# GPU设置
CUDA_VISIBLE_DEVICES=0
MODEL_CACHE_DIR=./models

# 其他设置
DEBUG=False
EOF
    echo "✅ 环境配置文件已创建"
fi

# 停止现有服务
echo "🛑 停止现有服务..."
docker-compose -f docker-compose.gpu.yml down || true

# 构建和启动服务
echo "🔨 构建Docker镜像..."
docker-compose -f docker-compose.gpu.yml build --no-cache

echo "🚀 启动服务..."
docker-compose -f docker-compose.gpu.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.gpu.yml ps

# 检查健康状态
echo "🏥 检查服务健康状态..."
sleep 10

# 检查后端健康状态
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 后端服务健康检查通过"
else
    echo "❌ 后端服务健康检查失败"
    docker-compose -f docker-compose.gpu.yml logs backend
fi

# 检查前端健康状态
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ 前端服务健康检查通过"
else
    echo "❌ 前端服务健康检查失败"
    docker-compose -f docker-compose.gpu.yml logs frontend
fi

# 检查Nginx状态
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Nginx代理健康检查通过"
else
    echo "❌ Nginx代理健康检查失败"
    docker-compose -f docker-compose.gpu.yml logs nginx
fi

echo "✅ 部署完成！"
echo ""
echo "📊 服务访问地址："
echo "   - 前端应用: http://117.50.198.126:3000"
echo "   - 后端API: http://117.50.198.126:8000"
echo "   - API文档: http://117.50.198.126:8000/docs"
echo "   - Nginx代理: http://117.50.198.126"
echo ""
echo "🔑 默认登录信息："
echo "   - 用户名: 李一御姐"
echo "   - 密码: 请使用您设置的密码"
echo ""
echo "🖥️  GPU信息："
echo "   - CUDA版本: 12.6"
echo "   - 框架版本: 2.7.1"
echo "   - Python版本: 3.12"
echo ""
echo "📝 管理命令："
echo "   - 查看日志: docker-compose -f docker-compose.gpu.yml logs -f"
echo "   - 停止服务: docker-compose -f docker-compose.gpu.yml down"
echo "   - 重启服务: docker-compose -f docker-compose.gpu.yml restart"
echo "   - 启动AI服务: docker-compose -f docker-compose.gpu.yml --profile ai up -d"
echo ""
echo "🎉 系统已成功部署到GPU服务器！"