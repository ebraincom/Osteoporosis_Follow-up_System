from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class UserType(str, enum.Enum):
    INSTITUTIONAL = "institutional"
    PERSONAL = "personal"



class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    
    # 用户类型相关字段
    user_type = Column(Enum(UserType), nullable=False)

    institution = Column(String(200))  # 机构名称或就诊机构
    department = Column(String(100))   # 科室名称（机构用户）
    
    # 个人用户特有字段
    age = Column(Integer)
    gender = Column(Enum(Gender))
    
    # 系统字段
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系 - 使用字符串引用避免循环导入
    patients = relationship("Patient", back_populates="user", lazy="dynamic")
    created_followups = relationship("FollowupRecord", back_populates="user", lazy="dynamic")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', user_type='{self.user_type}')>" 