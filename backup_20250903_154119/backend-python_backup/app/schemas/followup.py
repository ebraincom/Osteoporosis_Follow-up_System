from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FollowupRecordBase(BaseModel):
    """随访记录基础模型"""
    patient_id: int
    time: datetime
    method: str
    location: str
    details: str
    notes: Optional[str] = None
    patient_status: str
    next_followup_date: Optional[datetime] = None
    recommendations: Optional[str] = None

class FollowupRecordCreate(FollowupRecordBase):
    """创建随访记录模型"""
    pass

class FollowupRecordUpdate(BaseModel):
    """更新随访记录模型"""
    time: Optional[datetime] = None
    method: Optional[str] = None
    location: Optional[str] = None
    details: Optional[str] = None
    notes: Optional[str] = None
    patient_status: Optional[str] = None
    next_followup_date: Optional[datetime] = None
    recommendations: Optional[str] = None

class FollowupRecord(FollowupRecordBase):
    """随访记录响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FollowupRecordWithPatient(FollowupRecord):
    """包含患者信息的随访记录"""
    patient_name: str
    patient_patient_id: str 