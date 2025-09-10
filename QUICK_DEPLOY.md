# 🚀 快速部署命令

## 服务器信息
- **IP地址**: 117.50.198.126
- **系统**: Ubuntu 22.04 + CUDA 12.6 + Python 3.12
- **GPU**: 支持CUDA 12.6

## 一键部署命令

### 1. 连接到服务器
```bash
ssh root@117.50.198.126
```

### 2. 上传代码 (在本地执行)
```bash
# 使用rsync上传 (推荐)
rsync -avz --progress OsteoporosisFollow-upSystem_luhe/ root@117.50.198.126:/opt/osteoporosis-system/

# 或使用scp
scp -r OsteoporosisFollow-upSystem_luhe/ root@117.50.198.126:/opt/
```

### 3. 执行部署 (在服务器执行)
```bash
cd /opt/osteoporosis-system
chmod +x deploy_gpu_server.sh
./deploy_gpu_server.sh
```

## 访问地址

部署完成后，您可以通过以下地址访问系统：

- **前端应用**: http://117.50.198.126:3000
- **后端API**: http://117.50.198.126:8000
- **API文档**: http://117.50.198.126:8000/docs
- **Nginx代理**: http://117.50.198.126

## 管理命令

```bash
# 查看服务状态
docker-compose -f docker-compose.gpu.yml ps

# 查看日志
docker-compose -f docker-compose.gpu.yml logs -f

# 重启服务
docker-compose -f docker-compose.gpu.yml restart

# 停止服务
docker-compose -f docker-compose.gpu.yml down
```

## 登录信息

- **用户名**: 李一御姐
- **密码**: 使用您设置的密码

---

**部署完成后，您的骨质疏松症随访系统将在GPU服务器上运行，为将来集成大模型功能做好准备！** 🎉