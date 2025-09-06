from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, patients, reports, analytics, followups

api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(patients.router, prefix="/patients", tags=["患者管理"])
api_router.include_router(reports.router, prefix="/reports", tags=["报告管理"])
api_router.include_router(followups.router, prefix="/followups", tags=["随访管理"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["数据分析"]) 