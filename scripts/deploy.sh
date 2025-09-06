#!/bin/bash

# 骨质疏松症随访系统部署脚本

set -e

echo "🚀 开始部署骨质疏松症随访系统..."

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
mkdir -p uploads
mkdir -p nginx/ssl

# 复制环境配置文件
if [ ! -f backend-python/.env ]; then
    echo "📋 复制环境配置文件..."
    cp backend-python/env.example backend-python/.env
    echo "⚠️  请编辑 backend-python/.env 文件，配置正确的环境变量"
fi

# 构建和启动服务
echo "🔨 构建Docker镜像..."
docker-compose build

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 运行数据库迁移
echo "🗄️  运行数据库迁移..."
docker-compose exec backend alembic upgrade head

# 创建超级用户（可选）
echo "👤 创建超级用户..."
docker-compose exec backend python -c "
from app.core.database import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.models.user import UserType

db = SessionLocal()
try:
    # 检查是否已存在管理员用户
    admin = db.query(User).filter(User.username == 'admin').first()
    if not admin:
        admin_user = UserCreate(
            username='admin',
            email='admin@example.com',
            password='admin123',
            name='系统管理员',
            user_type=UserType.INSTITUTIONAL,
            institution='系统管理'
        )
        create_user(db, admin_user)
        print('✅ 超级用户创建成功')
    else:
        print('ℹ️  超级用户已存在')
finally:
    db.close()
"

echo "✅ 部署完成！"
echo ""
echo "📊 服务访问地址："
echo "   - 前端应用: http://localhost:3000"
echo "   - 后端API: http://localhost:8000"
echo "   - API文档: http://localhost:8000/docs"
echo "   - Flower监控: http://localhost:5555"
echo ""
echo "🔑 默认登录信息："
echo "   - 用户名: admin"
echo "   - 密码: admin123"
echo ""
echo "📝 查看日志："
echo "   - docker-compose logs -f"
echo ""
echo "🛑 停止服务："
echo "   - docker-compose down" 