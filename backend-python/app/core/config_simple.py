from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "骨质疏松症随访系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 环境配置
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 安全配置
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 数据库配置 - 使用SQLite
    DATABASE_URL: str = "sqlite:///./osteoporosis.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS配置
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"]
    
    # 邮件配置
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    
    # LLM配置
    LLM_API_KEY: Optional[str] = None
    LLM_API_URL: Optional[str] = None
    LLM_MODEL: str = "gpt-3.5-turbo"

    # AI模型配置
    QWEN_API_KEY: Optional[str] = None
    QWEN_MODEL: str = "qwen-turbo"
    QWEN_MAX_TOKENS: int = 1000
    QWEN_TEMPERATURE: float = 0.7
    
    # Google Gemini配置
    GEMINI_API_KEY: Optional[str] = "AIzaSyBrBg9qqSX7noALfTrjTsJwJj6KmNdDEng"
    GEMINI_MODEL: str = "gemini-pro"
    
    
    # 豆包AI配置 (火山引擎)
    DOUBAO_API_KEY: Optional[str] = None
    DOUBAO_MODEL: str = "doubao-1-5-pro-32k-250115"
    DOUBAO_MAX_TOKENS: int = 1000
    DOUBAO_TEMPERATURE: float = 0.7
    
    # 语音交互配置 (火山引擎实时语音识别)
    VOICE_API_KEY: Optional[str] = "MrAVT4yIYi2iGTa2YBsPVtrGX8b6RX5L"
    VOICE_APP_ID: Optional[str] = "8906942357"
    VOICE_ENDPOINT_ID: Optional[str] = None
    VOICE_MODEL: str = "doubao-1-5-pro-32k-250115"
    VOICE_SAMPLE_RATE: int = 16000
    VOICE_CHANNELS: int = 1
    # 火山引擎实时语音识别API配置
    VOLCENGINE_ACCESS_KEY: Optional[str] = "MrAVT4yIYi2iGTa2YBsPVtrGX8b6RX5L"
    VOLCENGINE_SECRET_KEY: Optional[str] = "TldtLLEUW3pxBjtnCwUfy4XyFkjHmNzi"
    VOLCENGINE_REGION: str = "cn-beijing"
    
    # 监控配置
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = True
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 