from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime
from app.models.report import ReportType, ReportStatus


class ReportBase(BaseModel):
    """报告基础模型"""
    report_id: str
    patient_id: int
    report_type: ReportType
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    t_score: Optional[float] = None
    z_score: Optional[float] = None
    bone_density: Optional[float] = None
    risk_assessment: Optional[str] = None
    ai_analysis: Optional[str] = None
    ai_recommendations: Optional[str] = None

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

    @validator('bone_density')
    def validate_bone_density(cls, v):
        if v is not None and (v < 0 or v > 10):
            raise ValueError('骨密度值必须在0到10之间')
        return v

    @validator('file_size')
    def validate_file_size(cls, v):
        if v is not None and v < 0:
            raise ValueError('文件大小不能为负数')
        return v


class ReportCreate(ReportBase):
    """创建报告模型"""
    pass


class ReportUpdate(BaseModel):
    """更新报告模型"""
    report_id: Optional[str] = None
    patient_id: Optional[int] = None
    report_type: Optional[ReportType] = None
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    t_score: Optional[float] = None
    z_score: Optional[float] = None
    bone_density: Optional[float] = None
    risk_assessment: Optional[str] = None
    ai_analysis: Optional[str] = None
    ai_recommendations: Optional[str] = None
    status: Optional[ReportStatus] = None

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

    @validator('bone_density')
    def validate_bone_density(cls, v):
        if v is not None and (v < 0 or v > 10):
            raise ValueError('骨密度值必须在0到10之间')
        return v

    @validator('file_size')
    def validate_file_size(cls, v):
        if v is not None and v < 0:
            raise ValueError('文件大小不能为负数')
        return v


class Report(ReportBase):
    """报告响应模型"""
    id: int
    user_id: int
    status: ReportStatus
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportList(BaseModel):
    """报告列表响应模型"""
    reports: list[Report]
    total: int
    page: int
    size: int
    pages: int


class ReportStatistics(BaseModel):
    """报告统计模型"""
    total_reports: int
    reports_by_type: dict[str, int]
    reports_by_status: dict[str, int]
    average_processing_time: float


class ReportUpload(BaseModel):
    """报告上传模型"""
    patient_id: int
    report_type: ReportType
    title: str
    description: Optional[str] = None


class AIAnalysisRequest(BaseModel):
    """AI分析请求模型"""
    report_id: int
    analysis_type: str = "comprehensive"  # comprehensive, risk_assessment, recommendations


class AIAnalysisResponse(BaseModel):
    """AI分析响应模型"""
    report_id: int
    ai_analysis: str
    ai_recommendations: str
    confidence_score: float
    processing_time: float 