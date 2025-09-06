# 🎯 API配置固化文档

## 📋 配置概述
本文档记录了骨质疏松症随访系统的API配置，这些配置已经过测试验证，请勿随意修改。

## 🔧 核心配置

### 1. 前端请求配置 (frontend/src/utils/request.ts)
```typescript
const request = axios.create({
  baseURL: '/api',  // ⚠️ 重要：不要修改这个值
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

### 2. Vite代理配置 (frontend/vite.config.ts)
```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // 后端服务地址
      changeOrigin: true,
      secure: false,
      rewrite: (path) => path,  // 保持路径不变
    }
  }
}
```

### 3. 后端路由配置 (backend-python/main.py)
```python
# 包含API路由
app.include_router(api_router, prefix="/api/v1")
```

## 📍 API路径规范

### 正确的API调用方式：
```typescript
// ✅ 正确：使用相对路径，让baseURL自动添加前缀
request.post('/v1/auth/login', data)
request.get('/v1/patients', { params })
request.put('/v1/patients/123', data)

// ❌ 错误：不要包含/api前缀
request.post('/api/v1/auth/login', data)  // 错误！
request.get('/api/v1/patients', { params })  // 错误！
```

### 请求流程：
```
前端调用: request.post('/v1/auth/login', data)
↓
baseURL添加: /api + /v1/auth/login
↓
最终请求: /api/v1/auth/login
↓
Vite代理拦截: /api 开头的请求
↓
转发到后端: http://localhost:8000/api/v1/auth/login
↓
后端路由匹配: /api/v1/auth/login ✅
```

## 🚨 重要注意事项

### 1. 不要修改的内容：
- `frontend/src/utils/request.ts` 中的 `baseURL: '/api'`
- `frontend/vite.config.ts` 中的代理配置
- `backend-python/main.py` 中的路由前缀

### 2. 修改API路径时的规则：
- 如果修改了 `baseURL`，必须同步修改所有API调用路径
- 如果修改了后端路由前缀，必须同步修改前端配置
- 如果修改了Vite代理配置，必须同步修改前端配置

### 3. 测试验证：
- 每次修改后都要测试登录功能
- 每次修改后都要测试患者列表加载
- 每次修改后都要检查网络请求的URL

## 🔍 常见问题排查

### 问题1：404错误
**可能原因：**
- API路径包含重复的 `/api` 前缀
- 后端服务未启动
- Vite代理配置错误

**排查步骤：**
1. 检查浏览器网络面板中的请求URL
2. 确认后端服务状态
3. 验证Vite代理配置

### 问题2：跨域错误
**可能原因：**
- Vite代理未正确配置
- 后端CORS配置问题

**排查步骤：**
1. 检查Vite代理配置
2. 确认后端CORS中间件配置
3. 验证请求是否通过代理

### 问题3：认证失败
**可能原因：**
- Token未正确传递
- 后端认证中间件问题

**排查步骤：**
1. 检查localStorage中的token
2. 验证请求头中的Authorization
3. 确认后端认证逻辑

## 📝 修改记录

| 日期 | 修改内容 | 修改原因 | 测试结果 |
|------|----------|----------|----------|
| 2025-09-02 | 修复API路径重复问题 | 解决404错误 | ✅ 通过 |
| 2025-09-02 | 固化配置文档 | 避免重复问题 | ✅ 完成 |

## 🎯 总结

**核心原则：**
1. **配置一致性**：前端、代理、后端配置必须保持一致
2. **最小修改**：只修改真正有问题的部分
3. **测试验证**：每次修改后都要测试
4. **文档记录**：记录所有配置和修改

**记住：** 这些配置已经过测试验证，请勿随意修改。如有问题，请先查看本文档，然后按照排查步骤进行诊断。 