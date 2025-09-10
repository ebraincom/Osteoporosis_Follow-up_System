# 骨质疏松症随访系统部署指南

## 🚀 快速部署

### 1. 服务器环境要求

**最低配置：**
- CPU: 2核心
- 内存: 4GB RAM
- 存储: 20GB 可用空间
- 操作系统: Ubuntu 20.04+ / CentOS 8+ / Debian 11+

**推荐配置：**
- CPU: 4核心
- 内存: 8GB RAM
- 存储: 50GB 可用空间
- 网络: 100Mbps带宽

### 2. 安装依赖

#### 安装Docker和Docker Compose

**Ubuntu/Debian:**
```bash
# 更新包管理器
sudo apt update

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker
```

**CentOS/RHEL:**
```bash
# 安装Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. 部署步骤

#### 步骤1: 上传代码到服务器
```bash
# 使用scp上传代码
scp -r OsteoporosisFollow-upSystem_luhe/ user@your-server-ip:/opt/

# 或使用git克隆
git clone <your-repo-url> /opt/osteoporosis-system
cd /opt/osteoporosis-system
```

#### 步骤2: 检查服务器环境
```bash
# 给脚本执行权限
chmod +x check_server_environment.sh

# 运行环境检查
./check_server_environment.sh
```

#### 步骤3: 配置环境变量
```bash
# 编辑生产环境配置
nano backend-python/.env

# 重要配置项：
# SECRET_KEY=your-super-secret-production-key-change-this
# DATABASE_URL=sqlite:///./osteoporosis.db
# ALLOWED_HOSTS=["*"]
```

#### 步骤4: 部署系统
```bash
# 给部署脚本执行权限
chmod +x deploy_production.sh

# 运行部署
./deploy_production.sh
```

### 4. 访问系统

部署完成后，您可以通过以下地址访问系统：

- **前端应用**: http://your-server-ip:3000
- **后端API**: http://your-server-ip:8000
- **API文档**: http://your-server-ip:8000/docs
- **Nginx代理**: http://your-server-ip

### 5. 配置域名和SSL（可选）

#### 配置域名
```bash
# 编辑nginx配置
nano nginx/nginx.conf

# 将 server_name _; 改为您的域名
server_name your-domain.com;
```

#### 配置SSL证书
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 6. 系统管理

#### 查看服务状态
```bash
docker-compose -f docker-compose.prod.yml ps
```

#### 查看日志
```bash
# 查看所有服务日志
docker-compose -f docker-compose.prod.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

#### 重启服务
```bash
# 重启所有服务
docker-compose -f docker-compose.prod.yml restart

# 重启特定服务
docker-compose -f docker-compose.prod.yml restart backend
```

#### 停止服务
```bash
docker-compose -f docker-compose.prod.yml down
```

#### 更新系统
```bash
# 拉取最新代码
git pull

# 重新构建和部署
./deploy_production.sh
```

### 7. 数据备份

#### 自动备份
系统已配置自动备份功能，备份文件存储在 `backend-python/backups/` 目录。

#### 手动备份
```bash
# 备份数据库
docker-compose -f docker-compose.prod.yml exec backend python auto_backup.py

# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz backend-python/uploads/
```

### 8. 故障排除

#### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tuln | grep :80
   
   # 停止占用端口的服务
   sudo systemctl stop apache2  # 或其他服务
   ```

2. **Docker权限问题**
   ```bash
   # 将用户添加到docker组
   sudo usermod -aG docker $USER
   # 重新登录或执行
   newgrp docker
   ```

3. **内存不足**
   ```bash
   # 查看内存使用
   free -h
   
   # 清理Docker缓存
   docker system prune -a
   ```

4. **服务无法启动**
   ```bash
   # 查看详细错误日志
   docker-compose -f docker-compose.prod.yml logs backend
   ```

### 9. 性能优化

#### 系统优化
```bash
# 增加文件描述符限制
echo "* soft nofile 65535" >> /etc/security/limits.conf
echo "* hard nofile 65535" >> /etc/security/limits.conf

# 优化内核参数
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65535" >> /etc/sysctl.conf
sysctl -p
```

#### Docker优化
```bash
# 配置Docker日志轮转
sudo nano /etc/docker/daemon.json
# 添加:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 10. 监控和维护

#### 设置监控
```bash
# 安装监控工具
sudo apt install htop iotop nethogs

# 设置定时任务检查服务状态
crontab -e
# 添加: */5 * * * * /opt/osteoporosis-system/check_services.bat
```

#### 定期维护
- 每周检查磁盘空间
- 每月更新系统包
- 定期备份数据
- 监控系统性能

---

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 检查日志文件
2. 确认服务器环境配置
3. 验证网络连接
4. 联系技术支持团队

**祝您部署顺利！** 🎉