# 骨质疏松症随访系统 - 项目结构

## 项目概述

基于LLM大模型的骨质疏松症患者跟踪随访系统，采用前后端分离架构，前端使用Vue3，后端使用Python FastAPI。

## 技术栈

### 前端技术栈
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Vite** - 快速构建工具
- **Element Plus** - Vue3 UI组件库
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理库
- **Axios** - HTTP客户端
- **ECharts** - 数据可视化图表库

### 后端技术栈
- **FastAPI** - 现代、快速的Web框架
- **SQLAlchemy** - Python SQL工具包和ORM
- **Alembic** - 数据库迁移工具
- **PostgreSQL** - 关系型数据库
- **Redis** - 内存数据库，用于缓存
- **JWT** - JSON Web Token认证
- **Celery** - 分布式任务队列
- **Pydantic** - 数据验证和序列化

### 部署技术栈
- **Docker** - 容器化平台
- **Docker Compose** - 多容器应用编排
- **Nginx** - 反向代理服务器
- **Flower** - Celery监控工具

## 项目结构

```
osteoporosis-followup-system/
├── frontend/                          # Vue3前端项目
│   ├── public/                        # 静态资源
│   ├── src/                           # 源代码
│   │   ├── api/                       # API接口
│   │   ├── components/                # 公共组件
│   │   ├── router/                    # 路由配置
│   │   ├── stores/                    # 状态管理
│   │   ├── types/                     # TypeScript类型定义
│   │   ├── utils/                     # 工具函数
│   │   ├── views/                     # 页面组件
│   │   ├── App.vue                    # 根组件
│   │   ├── main.ts                    # 入口文件
│   │   └── style.css                  # 全局样式
│   ├── package.json                   # 依赖配置
│   ├── vite.config.ts                 # Vite配置
│   ├── tsconfig.json                  # TypeScript配置
│   └── Dockerfile                     # Docker构建文件
│
├── backend-python/                    # FastAPI后端项目
│   ├── app/                           # 应用代码
│   │   ├── api/                       # API路由
│   │   │   └── v1/                    # API版本1
│   │   │       ├── endpoints/         # API端点
│   │   │       └── api.py             # 路由聚合
│   │   ├── core/                      # 核心配置
│   │   │   ├── config.py              # 配置管理
│   │   │   ├── database.py            # 数据库配置
│   │   │   ├── redis.py               # Redis配置
│   │   │   └── security.py            # 安全相关
│   │   ├── crud/                      # 数据库操作
│   │   ├── models/                    # 数据模型
│   │   ├── schemas/                   # Pydantic模型
│   │   └── services/                  # 业务逻辑
│   ├── alembic/                       # 数据库迁移
│   ├── main.py                        # 应用入口
│   ├── requirements.txt               # Python依赖
│   ├── Dockerfile                     # Docker构建文件
│   └── env.example                    # 环境变量示例
│
├── database/                          # 数据库相关
│   └── init.sql                       # 数据库初始化脚本
│
├── nginx/                             # Nginx配置
│   ├── nginx.conf                     # Nginx主配置
│   └── ssl/                           # SSL证书
│
├── scripts/                           # 部署脚本
│   └── deploy.sh                      # 部署脚本
│
├── docker-compose.yml                 # Docker Compose配置
├── README.md                          # 项目说明
└── PROJECT_STRUCTURE.md               # 项目结构说明
```

## 核心功能模块

### 1. 用户管理模块
- 用户注册/登录
- 机构用户和个人用户
- JWT身份认证
- 用户权限管理

### 2. 患者管理模块
- 患者信息管理
- 患者档案维护
- 患者搜索和筛选
- 患者风险评估

### 3. 报告管理模块
- 医疗报告上传
- 报告智能解析
- AI辅助分析
- 报告历史记录

### 4. 随访管理模块
- 随访计划制定
- 随访提醒系统
- 随访记录管理
- 随访效果评估

### 5. 数据分析模块
- 患者数据统计
- 趋势分析图表
- 风险评估报告
- 治疗效果分析

## 数据库设计

### 主要数据表
1. **users** - 用户表
2. **patients** - 患者表
3. **reports** - 报告表
4. **followups** - 随访表
5. **reminder_logs** - 提醒日志表
6. **system_logs** - 系统日志表

### 关键字段
- 骨密度T值、Z值
- 骨折风险等级
- 随访状态和类型
- AI分析结果
- 时间戳和审计字段

## 部署架构

### 开发环境
```bash
# 前端开发
cd frontend
npm install
npm run dev

# 后端开发
cd backend-python
pip install -r requirements.txt
uvicorn main:app --reload
```

### 生产环境
```bash
# 使用Docker Compose部署
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 服务端口
- 前端: 3000
- 后端API: 8000
- 数据库: 5432
- Redis: 6379
- Flower监控: 5555
- Nginx: 80/443

## 安全特性

1. **身份认证**: JWT令牌认证
2. **密码安全**: bcrypt加密
3. **CORS配置**: 跨域请求控制
4. **输入验证**: Pydantic数据验证
5. **SQL注入防护**: SQLAlchemy ORM
6. **文件上传安全**: 文件类型和大小限制

## 监控和日志

1. **应用监控**: 健康检查端点
2. **任务监控**: Flower监控界面
3. **日志记录**: 结构化日志
4. **错误追踪**: Sentry集成
5. **性能监控**: 请求响应时间

## 扩展功能

1. **AI集成**: LLM模型接入
2. **邮件通知**: 随访提醒邮件
3. **短信通知**: 短信提醒服务
4. **数据导出**: 报告导出功能
5. **移动端适配**: 响应式设计

## 开发规范

1. **代码规范**: ESLint + Prettier
2. **类型安全**: TypeScript严格模式
3. **API文档**: FastAPI自动生成
4. **测试覆盖**: 单元测试和集成测试
5. **版本控制**: Git工作流

## 性能优化

1. **数据库优化**: 索引和查询优化
2. **缓存策略**: Redis缓存
3. **异步处理**: Celery任务队列
4. **静态资源**: CDN加速
5. **代码分割**: 按需加载

这个项目结构提供了一个完整的、可扩展的骨质疏松症随访系统架构，支持从开发到生产的全流程部署。 