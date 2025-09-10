from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, patients, reports, analytics, followups, followup_responses, personal_auth, ai_qa, voice_interaction

api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(personal_auth.router, prefix="/personal-auth", tags=["个人用户认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(patients.router, prefix="/patients", tags=["患者管理"])
api_router.include_router(reports.router, prefix="/reports", tags=["报告管理"])
api_router.include_router(followups.router, prefix="/followups", tags=["随访管理"])
api_router.include_router(followup_responses.router, prefix="/followup-responses", tags=["随访应答"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["数据分析"])
api_router.include_router(ai_qa.router, prefix="/ai-qa", tags=["AI问答"])
api_router.include_router(voice_interaction.router, prefix="/voice", tags=["语音交互"]) 