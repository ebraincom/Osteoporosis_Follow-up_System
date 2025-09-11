from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
try:
    from app.core.config_simple import settings
except ImportError:
    from app.core.config_simple import settings
from app.schemas.personal_user import PersonalUserCreate, PersonalUser, PersonalUserLogin, PersonalUserLoginResponse
from app.crud.personal_user import get_personal_user_by_username, create_personal_user
from app.core.security import verify_password

router = APIRouter()

@router.post("/register", response_model=PersonalUserLoginResponse)
def register_personal_user(user: PersonalUserCreate, db: Session = Depends(get_db)):
    """个人用户注册"""
    try:
        # 检查个人用户表中是否已存在
        db_personal_user = get_personal_user_by_username(db, username=user.username)
        if db_personal_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 创建新个人用户
        new_user = create_personal_user(db=db, user=user)
    except Exception as e:
        print(f"个人用户注册错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"注册失败: {str(e)}"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username, "user_type": "personal"}, expires_delta=access_token_expires
    )
    
    # 创建刷新令牌
    refresh_token = create_refresh_token(data={"sub": new_user.username, "user_type": "personal"})
    
    # 返回包含用户信息和token的完整响应
    return {
        "token": access_token,
        "user": new_user,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/login", response_model=PersonalUserLoginResponse)
def login_personal_user(user_credentials: PersonalUserLogin, db: Session = Depends(get_db)):
    """个人用户登录"""
    # 验证用户
    user = get_personal_user_by_username(db, username=user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_type": "personal"}, expires_delta=access_token_expires
    )
    
    # 创建刷新令牌
    refresh_token = create_refresh_token(data={"sub": user.username, "user_type": "personal"})
    
    # 返回包含用户信息的完整响应
    return {
        "token": access_token,
        "user": user,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    } 