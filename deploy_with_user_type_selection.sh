#!/bin/bash

# 部署带有用户类型选择登录逻辑的版本到服务器

set -e

echo "🚀 开始部署带有用户类型选择登录逻辑的版本..."
echo "📍 服务器IP: 117.50.198.126"

# 检查必要文件
echo "🔍 检查必要文件..."
if [ ! -f "suifang.html" ]; then
    echo "❌ suifang.html 文件不存在"
    exit 1
fi

if [ ! -f "backend-python/app/api/v1/endpoints/personal_auth.py" ]; then
    echo "❌ 个人用户认证接口不存在"
    exit 1
fi

if [ ! -f "backend-python/app/models/personal_user.py" ]; then
    echo "❌ 个人用户模型不存在"
    exit 1
fi

echo "✅ 必要文件检查完成"

# 创建生产环境配置
echo "🔧 创建生产环境配置..."
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

echo "✅ 生产环境配置已创建"

# 初始化个人用户表
echo "🗄️  初始化个人用户表..."
cd backend-python
python init_personal_users_table.py
cd ..

echo "✅ 个人用户表初始化完成"

# 构建和部署
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
echo "🔑 登录功能："
echo "   - 支持机构用户和个人用户登录"
echo "   - 用户类型选择界面已更新"
echo "   - 个人用户专用界面已添加"
echo ""
echo "📝 管理命令："
echo "   - 查看日志: docker-compose -f docker-compose.gpu.yml logs -f"
echo "   - 停止服务: docker-compose -f docker-compose.gpu.yml down"
echo "   - 重启服务: docker-compose -f docker-compose.gpu.yml restart"
echo ""
echo "🎉 带有用户类型选择登录逻辑的版本已成功部署！"