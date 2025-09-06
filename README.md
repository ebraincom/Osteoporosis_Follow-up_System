# 骨质疏松症随访系统

## 项目概述

基于LLM大模型的骨质疏松症患者跟踪随访系统，提供高效的患者管理、科学干预和骨折风险降低服务。

## 技术架构

### 前端技术栈
- Vue 3 + TypeScript
- Vite
- Element Plus
- Vue Router
- Pinia
- Axios
- ECharts

### 后端技术栈
- #Spring Boot 3.x (Java方案)，最终没有采用
- FastAPI (Python方案)
- #MySQL 8.0 / PostgreSQL，最终采用SQLite
- Redis
- JWT认证

### 部署架构
- Nginx
- Docker
- Docker Compose
- Jenkins

## 项目结构

```
osteoporosis-followup-system/
├── frontend/                 # Vue3前端项目
├── backend-java/            # Spring Boot后端
├── backend-python/          # FastAPI后端
├── database/                # 数据库脚本
├── docker/                  # Docker配置
├── docs/                    # 文档
└── scripts/                 # 部署脚本
```

## 快速开始

### 开发环境
```bash
# 前端
cd frontend
npm install
npm run dev

# 后端 (Java)
cd backend-java
./mvnw spring-boot:run

# 后端 (Python)
cd backend-python
pip install -r requirements.txt
uvicorn main:app --reload
```

### 生产部署
```bash
docker-compose up -d
```

## 功能特性

- 用户管理（机构/个人用户）
- 患者信息管理
- 随访计划管理
- AI辅助诊断
- 数据统计分析
- 报告管理
- 提醒系统

## 开发团队

- 北京智芸数据提供技术支持 
