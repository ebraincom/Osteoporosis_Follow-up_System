# GPU服务器部署指南

## 🖥️ 服务器信息

**服务器配置：**
- **公网IP**: 117.50.198.126
- **操作系统**: Ubuntu 22.04
- **CUDA版本**: 12.6
- **框架版本**: 2.7.1 (PyTorch/TensorFlow)
- **Python版本**: 3.12
- **系统盘**: 200GB
- **GPU**: 支持CUDA 12.6的高性能GPU

## 🚀 快速部署步骤

### 1. 连接到服务器

```bash
# 使用SSH连接到服务器
ssh root@117.50.198.126
# 或
ssh your-username@117.50.198.126
```

### 2. 上传项目代码

**方法1: 使用SCP上传**
```bash
# 在本地执行，上传整个项目
scp -r OsteoporosisFollow-upSystem_luhe/ root@117.50.198.126:/opt/

# 或使用rsync (推荐)
rsync -avz --progress OsteoporosisFollow-upSystem_luhe/ root@117.50.198.126:/opt/osteoporosis-system/
```

**方法2: 使用Git克隆**
```bash
# 在服务器上执行
cd /opt
git clone <your-repo-url> osteoporosis-system
cd osteoporosis-system
```

### 3. 执行部署

```bash
# 进入项目目录
cd /opt/osteoporosis-system

# 给脚本执行权限
chmod +x deploy_gpu_server.sh

# 执行部署
./deploy_gpu_server.sh
```

### 4. 验证部署

部署完成后，访问以下地址验证：

- **前端应用**: http://117.50.198.126:3000
- **后端API**: http://117.50.198.126:8000
- **API文档**: http://117.50.198.126:8000/docs
- **Nginx代理**: http://117.50.198.126

## 🔧 系统管理

### 查看服务状态
```bash
# 查看所有服务
docker-compose -f docker-compose.gpu.yml ps

# 查看GPU使用情况
nvidia-smi

# 查看系统资源
htop
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose -f docker-compose.gpu.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose.gpu.yml logs -f backend
docker-compose -f docker-compose.gpu.yml logs -f frontend
```

### 重启服务
```bash
# 重启所有服务
docker-compose -f docker-compose.gpu.yml restart

# 重启特定服务
docker-compose -f docker-compose.gpu.yml restart backend
```

### 停止服务
```bash
docker-compose -f docker-compose.gpu.yml down
```

## 🤖 AI服务配置 (为将来大模型集成准备)

### 启动AI服务
```bash
# 启动包含AI服务的完整系统
docker-compose -f docker-compose.gpu.yml --profile ai up -d
```

### 测试GPU功能
```bash
# 测试CUDA是否正常工作
docker run --rm --gpus all nvidia/cuda:12.6-base-ubuntu22.04 nvidia-smi

# 测试PyTorch GPU支持
docker-compose -f docker-compose.gpu.yml exec backend python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## 🔒 安全配置

### 配置防火墙
```bash
# 安装UFW
sudo apt install ufw

# 配置防火墙规则
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 3000
sudo ufw allow 8000

# 启用防火墙
sudo ufw enable
```

### 配置SSL证书 (可选)
```bash
# 安装Certbot
sudo apt install certbot

# 获取SSL证书 (需要域名)
sudo certbot certonly --standalone -d your-domain.com

# 配置Nginx使用SSL
sudo nano nginx/nginx.conf
```

## 📊 性能监控

### 系统监控
```bash
# 安装监控工具
sudo apt install htop iotop nethogs

# 查看GPU使用情况
watch -n 1 nvidia-smi

# 查看系统资源
htop
```

### 应用监控
```bash
# 查看Docker容器资源使用
docker stats

# 查看特定容器日志
docker logs -f osteoporosis_backend_gpu
```

## 🔄 数据备份

### 自动备份
```bash
# 设置定时备份
crontab -e

# 添加以下内容 (每天凌晨2点备份)
0 2 * * * /opt/osteoporosis-system/backup_data.sh
```

### 手动备份
```bash
# 备份数据库
docker-compose -f docker-compose.gpu.yml exec backend python auto_backup.py

# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz backend-python/uploads/
```

## 🚨 故障排除

### 常见问题

1. **GPU不可用**
   ```bash
   # 检查NVIDIA驱动
   nvidia-smi
   
   # 检查Docker GPU支持
   docker run --rm --gpus all nvidia/cuda:12.6-base-ubuntu22.04 nvidia-smi
   ```

2. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tuln | grep :80
   
   # 停止占用端口的服务
   sudo systemctl stop apache2
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
   docker-compose -f docker-compose.gpu.yml logs backend
   ```

## 📈 性能优化

### GPU优化
```bash
# 设置GPU内存增长
export TF_FORCE_GPU_ALLOW_GROWTH=true
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
```

### 系统优化
```bash
# 增加文件描述符限制
echo "* soft nofile 65535" >> /etc/security/limits.conf
echo "* hard nofile 65535" >> /etc/security/limits.conf

# 优化内核参数
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65535" >> /etc/sysctl.conf
sysctl -p
```

## 🎯 下一步计划

1. **域名配置**: 配置域名指向服务器IP
2. **SSL证书**: 申请和配置SSL证书
3. **AI模型集成**: 集成大语言模型功能
4. **监控系统**: 部署完整的监控和告警系统
5. **负载均衡**: 配置多实例负载均衡

---

## 📞 技术支持

如果在部署过程中遇到问题：

1. 检查服务器日志: `docker-compose -f docker-compose.gpu.yml logs`
2. 验证GPU状态: `nvidia-smi`
3. 检查网络连接: `curl -I http://117.50.198.126:8000/health`
4. 联系技术支持团队

**祝您部署顺利！** 🎉