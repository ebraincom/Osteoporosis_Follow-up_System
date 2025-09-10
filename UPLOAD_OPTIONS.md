# 代码上传方案

## 方案1: 使用SCP (推荐)

```bash
# 在本地Windows PowerShell中执行
scp -r OsteoporosisFollow-upSystem_luhe/ root@117.50.198.126:/opt/
```

## 方案2: 使用Git (最简单)

在服务器上执行：
```bash
# 连接到服务器
ssh root@117.50.198.126

# 创建目录
mkdir -p /opt/osteoporosis-system
cd /opt/osteoporosis-system

# 如果您的代码在Git仓库中，直接克隆
git clone <your-repo-url> .

# 或者如果代码在本地，先推送到Git仓库
```

## 方案3: 使用WinSCP (图形界面)

1. 下载并安装WinSCP
2. 连接到服务器 117.50.198.126
3. 拖拽文件夹到服务器

## 方案4: 使用压缩包

在本地执行：
```bash
# 压缩项目
tar -czf osteoporosis-system.tar.gz OsteoporosisFollow-upSystem_luhe/

# 上传压缩包
scp osteoporosis-system.tar.gz root@117.50.198.126:/opt/

# 在服务器上解压
ssh root@117.50.198.126
cd /opt
tar -xzf osteoporosis-system.tar.gz
mv OsteoporosisFollow-upSystem_luhe osteoporosis-system
```

## 方案5: 安装rsync (如果您想使用rsync)

在服务器上执行：
```bash
# Ubuntu/Debian
apt update && apt install rsync

# CentOS/RHEL
yum install rsync
```

然后就可以使用rsync命令了。