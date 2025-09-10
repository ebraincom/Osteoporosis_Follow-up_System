from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class FollowupResponseBase(BaseModel):
    """随访应答基础模型"""
    followup_id: int
    overall_feeling: Optional[str] = None  # 总体感受
    improvement_level: Optional[str] = None  # 状况改善
    medication_adherence: Optional[str] = None  # 用药依从性
    exercise_volume: Optional[str] = None  # 运动量
    diet_adjustment: Optional[str] = None  # 饮食调整
    pain_level: Optional[int] = None  # 疼痛程度
    sleep_quality: Optional[str] = None  # 睡眠质量
    daily_activity: Optional[str] = None  # 日常活动能力
    mood_status: Optional[str] = None  # 情绪状态
    social_activity: Optional[str] = None  # 社交活动
    side_effects: Optional[str] = None  # 副作用
    concerns: Optional[str] = None  # 担忧
    suggestions: Optional[str] = None  # 建议
    additional_info: Optional[str] = None  # 其他信息

    @validator('pain_level')
    def validate_pain_level(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('疼痛程度必须在1-10之间')
        return v


class FollowupResponseCreate(FollowupResponseBase):
    """创建随访应答模型"""
    is_completed: Optional[bool] = None


class FollowupResponseUpdate(BaseModel):
    """更新随访应答模型"""
    overall_feeling: Optional[str] = None
    improvement_level: Optional[str] = None
    medication_adherence: Optional[str] = None
    exercise_volume: Optional[str] = None
    diet_adjustment: Optional[str] = None
    pain_level: Optional[int] = None
    sleep_quality: Optional[str] = None
    daily_activity: Optional[str] = None
    mood_status: Optional[str] = None
    social_activity: Optional[str] = None
    side_effects: Optional[str] = None
    concerns: Optional[str] = None
    suggestions: Optional[str] = None
    additional_info: Optional[str] = None
    is_completed: Optional[bool] = None

    @validator('pain_level')
    def validate_pain_level(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('疼痛程度必须在1-10之间')
        return v


class FollowupResponse(FollowupResponseBase):
    """随访应答响应模型"""
    id: int
    patient_id: int
    response_time: datetime
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FollowupResponseWithPatient(FollowupResponse):
    """包含患者信息的随访应答模型"""
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None


class FollowupResponseList(BaseModel):
    """随访应答列表响应模型"""
    responses: list[FollowupResponse]
    total: int
    page: int
    size: int
    pages: int