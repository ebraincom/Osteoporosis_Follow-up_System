#!/bin/bash

# 服务器环境检查脚本

echo "🔍 检查服务器环境..."

# 检查操作系统
echo "📋 操作系统信息："
cat /etc/os-release | head -5

# 检查系统资源
echo ""
echo "💻 系统资源："
echo "CPU核心数: $(nproc)"
echo "内存大小: $(free -h | grep '^Mem:' | awk '{print $2}')"
echo "磁盘空间: $(df -h / | tail -1 | awk '{print $4}')"

# 检查Docker
echo ""
echo "🐳 Docker检查："
if command -v docker &> /dev/null; then
    echo "✅ Docker已安装: $(docker --version)"
    if docker info &> /dev/null; then
        echo "✅ Docker服务运行正常"
    else
        echo "❌ Docker服务未运行"
    fi
else
    echo "❌ Docker未安装"
fi

# 检查Docker Compose
echo ""
echo "🐙 Docker Compose检查："
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose已安装: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    echo "✅ Docker Compose (新版本)已安装: $(docker compose version)"
else
    echo "❌ Docker Compose未安装"
fi

# 检查网络
echo ""
echo "🌐 网络检查："
echo "公网IP: $(curl -s ifconfig.me || echo '无法获取')"
echo "内网IP: $(hostname -I | awk '{print $1}')"

# 检查端口占用
echo ""
echo "🔌 端口占用检查："
for port in 80 443 3000 8000; do
    if netstat -tuln | grep ":$port " > /dev/null; then
        echo "⚠️  端口 $port 已被占用"
    else
        echo "✅ 端口 $port 可用"
    fi
done

# 检查防火墙
echo ""
echo "🔥 防火墙检查："
if command -v ufw &> /dev/null; then
    echo "UFW状态: $(ufw status | head -1)"
elif command -v firewall-cmd &> /dev/null; then
    echo "Firewalld状态: $(firewall-cmd --state 2>/dev/null || echo '未运行')"
else
    echo "未检测到常见防火墙"
fi

# 检查SSL证书工具
echo ""
echo "🔐 SSL证书工具检查："
if command -v certbot &> /dev/null; then
    echo "✅ Certbot已安装"
else
    echo "ℹ️  Certbot未安装（可选，用于SSL证书）"
fi

echo ""
echo "✅ 环境检查完成！"