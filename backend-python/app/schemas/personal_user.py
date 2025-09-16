from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from app.models.personal_user import Gender

# 基础个人用户模型
class PersonalUserBase(BaseModel):
    username: str
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    institution: Optional[str] = None
    # 添加更多字段
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    t_score: Optional[float] = None
    z_score: Optional[float] = None
    risk_level: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    family_history: Optional[str] = None
    medications: Optional[str] = None

# 创建个人用户
class PersonalUserCreate(PersonalUserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度至少6位')
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 1 or v > 120):
            raise ValueError('年龄必须在1-120之间')
        return v

# 更新个人用户
class PersonalUserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    institution: Optional[str] = None
    avatar: Optional[str] = None
    # 添加更多字段支持
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    t_score: Optional[float] = None
    z_score: Optional[float] = None
    risk_level: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    family_history: Optional[str] = None
    medications: Optional[str] = None

# 个人用户响应
class PersonalUser(PersonalUserBase):
    id: int
    user_type: str = "personal"  # 添加用户类型字段
    is_active: bool
    is_verified: bool
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 个人用户登录响应
class PersonalUserLoginResponse(BaseModel):
    token: str
    user: PersonalUser
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# 个人用户登录请求
class PersonalUserLogin(BaseModel):
    username: str
    password: str 