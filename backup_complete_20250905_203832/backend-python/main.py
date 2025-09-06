from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

# 统一使用config_simple配置
try:
    from app.core.config_simple import settings
except ImportError:
    from app.core.config import settings

# 导入模型以确保它们被正确初始化
from app.models import user, patient, followup, report

from app.api.v1.api import api_router
from app.core.database import engine
from app.core.redis import redis_client

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="骨质疏松症随访系统API",
    description="基于LLM的骨质疏松症患者跟踪随访系统后端API",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 修复TrustedHostMiddleware配置 - 使用主机名而不是URL
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Process Time: {process_time:.4f}s"
    )
    
    return response

# 异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT
    }

# 包含API路由
app.include_router(api_router, prefix="/api/v1")

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    logger.info("Application startup complete")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
    # 暂时注释掉关闭逻辑，避免错误
    # if engine:
    #     await engine.dispose()
    # if redis_client:
    #     await redis_client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 启用reload以便开发
        log_level="info"
    ) 