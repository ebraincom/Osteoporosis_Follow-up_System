from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserType, Gender

# 基础用户模型
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None  # 改为可选
    name: str
    phone: Optional[str] = None
    user_type: UserType

    institution: Optional[str] = None
    department: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None

# 创建用户
class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度至少6位')
        return v

# 更新用户
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    avatar: Optional[str] = None

# 用户响应
class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 登录响应
class LoginResponse(BaseModel):
    token: str
    user: User
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# 登录请求
class UserLogin(BaseModel):
    username: str
    password: str

# 令牌响应
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# 令牌数据
class TokenData(BaseModel):
    username: Optional[str] = None 