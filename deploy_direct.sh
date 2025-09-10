#!/bin/bash

# 骨质疏松症随访系统直接部署脚本 (无Docker版本)
# 服务器IP: 117.50.198.126

set -e

echo "🚀 开始直接部署骨质疏松症随访系统..."
echo "📍 服务器IP: 117.50.198.126"
echo "🖥️  系统配置: Ubuntu 22.04 + CUDA 12.6 + Python 3.12"

# 更新系统
echo "📦 更新系统包..."
apt update

# 安装必要的依赖
echo "🔧 安装系统依赖..."
apt install -y python3-pip python3-venv nodejs npm nginx sqlite3

# 进入项目目录
cd /opt/osteoporosis-system

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
cd backend-python
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo "📚 安装Python依赖..."
pip install -r requirements.txt

# 创建环境配置文件
echo "📋 创建环境配置..."
cat > .env << EOF
ENVIRONMENT=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./osteoporosis.db
ALLOWED_HOSTS=["*"]
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads
DEBUG=False
EOF

# 创建必要的目录
mkdir -p uploads backups

# 启动后端服务
echo "🚀 启动后端服务..."
nohup python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务PID: $BACKEND_PID"

# 等待后端启动
sleep 10

# 检查后端健康状态
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    cat ../logs/backend.log
    exit 1
fi

# 安装Node.js依赖
echo "📦 安装Node.js依赖..."
cd ../frontend
npm install

# 构建前端
echo "🔨 构建前端..."
npm run build

# 配置Nginx
echo "🌐 配置Nginx..."
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80;
    server_name _;
    root /opt/osteoporosis-system/frontend/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 重启Nginx
systemctl restart nginx

# 检查服务状态
echo "🔍 检查服务状态..."
sleep 5

if curl -f http://localhost/ > /dev/null 2>&1; then
    echo "✅ 前端服务启动成功"
else
    echo "❌ 前端服务启动失败"
fi

echo "✅ 部署完成！"
echo ""
echo "📊 服务访问地址："
echo "   - 前端应用: http://117.50.198.126"
echo "   - 后端API: http://117.50.198.126:8000"
echo "   - API文档: http://117.50.198.126:8000/docs"
echo ""
echo "🔑 默认登录信息："
echo "   - 用户名: 李一御姐"
echo "   - 密码: 请使用您设置的密码"
echo ""
echo "📝 管理命令："
echo "   - 查看后端日志: tail -f /opt/osteoporosis-system/logs/backend.log"
echo "   - 重启后端: pkill -f 'python main.py' && cd /opt/osteoporosis-system/backend-python && nohup python main.py > ../logs/backend.log 2>&1 &"
echo "   - 重启Nginx: systemctl restart nginx"
echo ""
echo "🎉 系统已成功部署！"