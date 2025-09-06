from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("male", "female"), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    
    # 医疗信息
    height = Column(Float)  # 身高(cm)
    weight = Column(Float)  # 体重(kg)
    bmi = Column(Float)     # BMI指数
    
    # 骨密度相关
    t_score = Column(Float)  # T值
    z_score = Column(Float)  # Z值
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    
    # 病史
    medical_history = Column(Text)
    family_history = Column(Text)
    medications = Column(Text)
    
    # 关联用户（医生/机构）
    user_id = Column(Integer, ForeignKey("users.id"))
    # 关联关系 - 使用字符串引用避免循环导入
    user = relationship("User", back_populates="patients")
    followup_records = relationship("FollowupRecord", back_populates="patient", cascade="all, delete-orphan")
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Patient(id={self.id}, patient_id='{self.patient_id}', name='{self.name}')>" 