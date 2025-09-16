from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class PersonalUser(Base):
    __tablename__ = "personal_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)  # 可选
    age = Column(Integer, nullable=True)       # 可选
    gender = Column(Enum(Gender), nullable=True)  # 可选
    institution = Column(String(200), nullable=True)  # 就诊机构，可选
    
    # 添加更多字段
    email = Column(String(100), nullable=True)
    height = Column(Float, nullable=True)  # 身高(cm)
    weight = Column(Float, nullable=True)  # 体重(kg)
    t_score = Column(Float, nullable=True)  # T值
    z_score = Column(Float, nullable=True)  # Z值
    risk_level = Column(String(20), nullable=True)  # 风险等级
    address = Column(Text, nullable=True)  # 地址
    medical_history = Column(Text, nullable=True)  # 现病史
    family_history = Column(Text, nullable=True)  # 家族史
    medications = Column(Text, nullable=True)  # 用药史
    
    # 系统字段
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系 - 暂时注释掉，避免外键约束问题
    # patients = relationship("Patient", back_populates="personal_user", lazy="dynamic")
    # created_followups = relationship("FollowupRecord", back_populates="personal_user", lazy="dynamic")
    
    def __repr__(self):
        return f"<PersonalUser(id={self.id}, username='{self.username}', name='{self.name}')>" 