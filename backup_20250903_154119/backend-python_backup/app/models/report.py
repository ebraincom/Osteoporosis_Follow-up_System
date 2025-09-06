from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ReportType(str, enum.Enum):
    DXA = "dxa"           # 骨密度检查
    CT = "ct"             # CT检查
    XRAY = "xray"         # X光检查
    BLOOD = "blood"       # 血液检查
    OTHER = "other"       # 其他检查

class ReportStatus(str, enum.Enum):
    PENDING = "pending"       # 待处理
    PROCESSING = "processing" # 处理中
    COMPLETED = "completed"   # 已完成
    ERROR = "error"          # 处理错误

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(50), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 报告基本信息
    report_type = Column(Enum(ReportType), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))  # 文件存储路径
    file_size = Column(Integer)      # 文件大小(bytes)
    
    # 检查结果
    t_score = Column(Float)
    z_score = Column(Float)
    bone_density = Column(Float)  # 骨密度值
    risk_assessment = Column(Text) # 风险评估
    
    # AI分析结果
    ai_analysis = Column(Text)     # AI分析结果
    ai_recommendations = Column(Text) # AI建议
    
    # 状态管理
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    processing_start_time = Column(DateTime(timezone=True))
    processing_end_time = Column(DateTime(timezone=True))
    
    # 关联关系 - 暂时注释掉，避免循环导入问题
    # patient = relationship("Patient", back_populates="reports")
    # user = relationship("User", back_populates="reports")
    
    # 系统字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Report(id={self.id}, report_id='{self.report_id}', type='{self.report_type}')>" 