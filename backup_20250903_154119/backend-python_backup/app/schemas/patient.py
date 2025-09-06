from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from app.models.patient import RiskLevel, Gender


class PatientBase(BaseModel):
    """患者基础模型"""
    patient_id: str
    name: str
    age: int
    gender: Gender
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    bmi: Optional[float] = None
    t_score: Optional[float] = None
    z_score: Optional[float] = None
    risk_level: Optional[RiskLevel] = RiskLevel.LOW
    medical_history: Optional[str] = None
    family_history: Optional[str] = None
    medications: Optional[str] = None

    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('年龄必须在0-150之间')
        return v

    @validator('height')
    def validate_height(cls, v):
        if v is not None and (v < 50 or v > 300):
            raise ValueError('身高必须在50-300cm之间')
        return v

    @validator('weight')
    def validate_weight(cls, v):
        if v is not None and (v < 10 or v > 500):
            raise ValueError('体重必须在10-500kg之间')
        return v

    @validator('bmi')
    def validate_bmi(cls, v):
        if v is not None and (v < 10 or v > 100):
            raise ValueError('BMI必须在10-100之间')
        return v

    @validator('t_score')
    def validate_t_score(cls, v):
        if v is not None and (v < -10 or v > 10):
            raise ValueError('T值必须在-10到10之间')
        return v

    @validator('z_score')
    def validate_z_score(cls, v):
        if v is not None and (v < -10 or v > 10):
            raise ValueError('Z值必须在-10到10之间')
        return v


class PatientCreate(PatientBase):
    """创建患者模型"""
    pass


class PatientUpdate(BaseModel):
    """更新患者模型"""
    patient_id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    bmi: Optional[float] = None
    t_score: Optional[float] = None
    z_score: Optional[float] = None
    risk_level: Optional[RiskLevel] = None
    medical_history: Optional[str] = None
    family_history: Optional[str] = None
    medications: Optional[str] = None

    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError('年龄必须在0-150之间')
        return v

    @validator('height')
    def validate_height(cls, v):
        if v is not None and (v < 50 or v > 300):
            raise ValueError('身高必须在50-300cm之间')
        return v

    @validator('weight')
    def validate_weight(cls, v):
        if v is not None and (v < 10 or v > 500):
            raise ValueError('体重必须在10-500kg之间')
        return v

    @validator('bmi')
    def validate_bmi(cls, v):
        if v is not None and (v < 10 or v > 100):
            raise ValueError('BMI必须在10-100之间')
        return v

    @validator('t_score')
    def validate_t_score(cls, v):
        if v is not None and (v < -10 or v > 10):
            raise ValueError('T值必须在-10到10之间')
        return v

    @validator('z_score')
    def validate_z_score(cls, v):
        if v is not None and (v < -10 or v > 10):
            raise ValueError('Z值必须在-10到10之间')
        return v


class Patient(PatientBase):
    """患者响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PatientList(BaseModel):
    """患者列表响应模型"""
    patients: list[Patient]
    total: int
    page: int
    size: int
    pages: int


class PatientRiskAssessment(BaseModel):
    """患者风险评估模型"""
    patient_id: int
    t_score: float
    z_score: float
    risk_level: RiskLevel
    assessment_date: datetime
    recommendations: Optional[str] = None


class PatientStatistics(BaseModel):
    """患者统计模型"""
    total_patients: int
    patients_by_risk_level: dict[str, int]
    patients_by_age_group: dict[str, int]
    patients_by_gender: dict[str, int]
    average_age: float
    average_bmi: Optional[float] = None
    average_t_score: Optional[float] = None
    average_z_score: Optional[float] = None 