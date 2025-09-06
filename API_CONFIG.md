# API配置固化说明

## 🎯 配置原则
- **简单直接**：避免复杂的路径重写和转换
- **一一对应**：前端路径与后端路径完全一致
- **稳定可靠**：配置一次，长期有效

## 📋 固化配置

### 前端配置

#### 1. Axios配置 (`frontend/src/utils/request.ts`)
```typescript
const request = axios.create({
  baseURL: '',  // 不使用baseURL，直接使用完整路径
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

#### 2. API调用 (`frontend/src/api/auth.ts`)
```typescript
export const authApi = {
  login: (data: LoginForm): Promise<AuthResponse> => {
    return request.post('/api/v1/auth/login', data)
  },

  register: (data: RegisterForm): Promise<AuthResponse> => {
    const backendData = {
      ...data,
      user_type: data.userType,  // 字段名转换
      confirmPassword: undefined
    }
    delete backendData.confirmPassword
    return request.post('/api/v1/auth/register', backendData)
  },

  getCurrentUser: (): Promise<User> => {
    return request.get('/api/v1/users/me')
  },

  refreshToken: (): Promise<{ token: string }> => {
    return request.post('/api/v1/auth/refresh')
  },

  logout: (): Promise<void> => {
    return request.post('/api/v1/auth/logout')
  }
}
```

#### 3. Vite代理配置 (`frontend/vite.config.ts`)
```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      // 不重写路径，直接转发到后端
    },
  },
},
```

### 后端配置

#### 1. 路由前缀 (`backend-python/main_simple.py`)
```python
# 包含API路由
try:
    from app.api.v1.api import api_router
    app.include_router(api_router, prefix="/api/v1")
    logger.info("API路由已加载")
except ImportError as e:
    logger.warning(f"无法加载API路由: {e}")
```

#### 2. 数据库配置 (`backend-python/app/core/database.py`)
```python
try:
    from app.core.config_simple import settings
except ImportError:
    from app.core.config import settings
```

## 🔄 请求流程

1. **前端发送请求**：`POST /api/v1/auth/register`
2. **Vite代理转发**：`http://localhost:3000/api/v1/auth/register` → `http://localhost:8000/api/v1/auth/register`
3. **后端接收处理**：FastAPI路由 `/api/v1/auth/register`

## ✅ 验证方法

### 1. 检查服务状态
```bash
.\check_services.bat
```

### 2. 测试API连接
```bash
# 健康检查
curl http://localhost:8000/health

# 注册测试
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123","name":"测试用户","user_type":"institutional","institution":"测试机构"}'
```

### 3. 前端测试
- 访问：http://localhost:3000
- 尝试注册新用户
- 检查浏览器控制台网络请求

## 🚫 禁止修改

以下配置已固化，请勿随意修改：

1. **前端baseURL**：必须为空字符串
2. **API路径**：必须使用完整路径 `/api/v1/...`
3. **代理配置**：只处理 `/api` 路径，不重写
4. **后端路由前缀**：必须为 `/api/v1`

## 🔧 故障排除

### 问题1：404 Not Found
- 检查后端服务是否运行
- 确认API路径是否正确
- 验证代理配置

### 问题2：500 Internal Server Error
- 检查数据库是否初始化
- 查看后端日志
- 确认字段映射是否正确

### 问题3：CORS错误
- 确认后端CORS配置
- 检查代理设置

## 📝 更新记录

- 2025-08-28：固化API配置，解决路径重复问题
- 配置原则：简单直接，避免复杂转换 