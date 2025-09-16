from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# 统一使用config_simple配置
try:
    from app.core.config_simple import settings
except ImportError:
    from app.core.config_simple import settings

from app.core.database import get_db

# 密码加密上下文 - 使用更兼容的配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# OAuth2 scheme for token extraction - 统一在这里定义
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token: str) -> Optional[dict]:
    """获取当前用户信息"""
    payload = verify_token(token)
    if payload is None:
        return None
    return payload

def get_current_active_user(token: str) -> Optional[dict]:
    """获取当前活跃用户信息"""
    user = get_current_user(token)
    if user is None:
        return None
    # 这里可以添加额外的用户状态检查
    return user

# FastAPI dependency for authentication
def get_current_user_dependency(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """FastAPI依赖：获取当前用户"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"=== 开始验证token ===")
    logger.info(f"Token长度: {len(token) if token else 0}")
    logger.info(f"Token前20字符: {token[:20] if token else 'None'}...")
    logger.info(f"当前SECRET_KEY: {settings.SECRET_KEY[:20]}...")
    logger.info(f"当前ALGORITHM: {settings.ALGORITHM}")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        logger.info(f"Token解码成功，用户名: {username}")
        logger.info(f"完整payload: {payload}")
        
        if username is None:
            logger.error("Token中没有用户名")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Token解码失败: {e}")
        logger.error(f"Token内容: {token}")
        logger.error(f"SECRET_KEY: {settings.SECRET_KEY}")
        raise credentials_exception
    
    # 避免循环导入，直接在这里查询用户
    # 首先尝试查询机构用户表
    from app.models.user import User
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        # 如果机构用户表中没有，尝试查询个人用户表
        from app.models.personal_user import PersonalUser
        personal_user = db.query(PersonalUser).filter(PersonalUser.username == username).first()
        if personal_user is None:
            logger.error(f"用户不存在: {username}")
            raise credentials_exception
        else:
            logger.info(f"个人用户验证成功: {personal_user.username}, ID: {personal_user.id}")
            logger.info(f"=== Token验证完成 ===")
            return personal_user
    else:
        logger.info(f"机构用户验证成功: {user.username}, ID: {user.id}")
        logger.info(f"=== Token验证完成 ===")
        return user 