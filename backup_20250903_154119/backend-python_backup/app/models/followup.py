from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class FollowupRecord(Base):
    __tablename__ = "followup_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 创建随访记录的医生
    
    # 随访基本信息
    time = Column(DateTime, nullable=False, default=func.now())
    method = Column(String(100), nullable=False)  # 随访方式
    location = Column(String(200), nullable=False)  # 随访地点
    details = Column(Text, nullable=False)  # 随访内容
    notes = Column(Text)  # 医生备注
    
    # 随访结果
    patient_status = Column(String(100), nullable=False)  # 患者状态
    next_followup_date = Column(DateTime)  # 下次随访时间
    recommendations = Column(Text)  # 治疗建议
    
    # 时间戳
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系 - 使用字符串引用避免循环导入
    patient = relationship("Patient", back_populates="followup_records")
    user = relationship("User", back_populates="created_followups")
    
    def __repr__(self):
        return f"<FollowupRecord(id={self.id}, patient_id={self.patient_id}, time={self.time})>" 