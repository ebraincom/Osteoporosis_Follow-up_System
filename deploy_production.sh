#!/bin/bash

# 骨质疏松症随访系统生产环境部署脚本

set -e

echo "🚀 开始部署骨质疏松症随访系统到生产环境..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs
mkdir -p nginx/ssl
mkdir -p backend-python/uploads
mkdir -p backend-python/backups

# 检查环境配置文件
if [ ! -f backend-python/.env.production ]; then
    echo "📋 创建生产环境配置文件..."
    cp backend-python/.env.production backend-python/.env
    echo "⚠️  请编辑 backend-python/.env 文件，配置正确的环境变量"
    echo "⚠️  特别是 SECRET_KEY 需要设置为安全的随机字符串"
fi

# 停止现有服务
echo "🛑 停止现有服务..."
docker-compose -f docker-compose.prod.yml down || true

# 构建和启动服务
echo "🔨 构建Docker镜像..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo "🚀 启动服务..."
docker-compose -f docker-compose.prod.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.prod.yml ps

# 检查健康状态
echo "🏥 检查服务健康状态..."
sleep 10

# 检查后端健康状态
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 后端服务健康检查通过"
else
    echo "❌ 后端服务健康检查失败"
    docker-compose -f docker-compose.prod.yml logs backend
fi

# 检查前端健康状态
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ 前端服务健康检查通过"
else
    echo "❌ 前端服务健康检查失败"
    docker-compose -f docker-compose.prod.yml logs frontend
fi

# 检查Nginx状态
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Nginx代理健康检查通过"
else
    echo "❌ Nginx代理健康检查失败"
    docker-compose -f docker-compose.prod.yml logs nginx
fi

echo "✅ 部署完成！"
echo ""
echo "📊 服务访问地址："
echo "   - 前端应用: http://your-server-ip:3000"
echo "   - 后端API: http://your-server-ip:8000"
echo "   - API文档: http://your-server-ip:8000/docs"
echo "   - Nginx代理: http://your-server-ip"
echo ""
echo "🔑 默认登录信息："
echo "   - 用户名: 李一御姐"
echo "   - 密码: 请使用您设置的密码"
echo ""
echo "📝 查看日志："
echo "   - docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🛑 停止服务："
echo "   - docker-compose -f docker-compose.prod.yml down"
echo ""
echo "🔄 重启服务："
echo "   - docker-compose -f docker-compose.prod.yml restart"