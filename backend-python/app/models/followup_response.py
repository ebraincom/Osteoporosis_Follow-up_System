from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class FollowupResponse(Base):
    """患者随访应答模型"""
    __tablename__ = "followup_responses"

    id = Column(Integer, primary_key=True, index=True)
    followup_id = Column(Integer, ForeignKey("followup_records.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    
    # 应答基本信息
    response_time = Column(DateTime, nullable=False, default=func.now())  # 应答时间
    is_completed = Column(Boolean, default=False)  # 是否完成应答
    
    # 患者自评指标
    overall_feeling = Column(String(100))  # 总体感受：良好/一般/较差
    improvement_level = Column(String(100))  # 状况改善：明显改善/有所改善/改善不明显/无改善
    medication_adherence = Column(String(100))  # 用药依从性：完全按照医嘱/基本按照医嘱/有时忘记服药/经常忘记服药
    exercise_volume = Column(Text)  # 运动量描述
    diet_adjustment = Column(Text)  # 饮食调整描述
    
    # 症状评估
    pain_level = Column(Integer)  # 疼痛程度 1-10分
    sleep_quality = Column(String(100))  # 睡眠质量：很好/一般/较差
    daily_activity = Column(String(100))  # 日常活动能力：正常/轻度受限/中度受限/重度受限
    
    # 生活质量评估
    mood_status = Column(String(100))  # 情绪状态：积极/一般/消极
    social_activity = Column(String(100))  # 社交活动：正常/减少/很少参与
    
    # 其他反馈
    side_effects = Column(Text)  # 副作用描述
    concerns = Column(Text)  # 担忧或问题
    suggestions = Column(Text)  # 建议或意见
    additional_info = Column(Text)  # 其他补充信息
    
    # 时间戳
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联关系
    followup_record = relationship("FollowupRecord", back_populates="responses")
    patient = relationship("Patient", back_populates="followup_responses")
    
    def __repr__(self):
        return f"<FollowupResponse(id={self.id}, followup_id={self.followup_id}, patient_id={self.patient_id})>"