from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import patient as patient_crud
from app.crud import report as report_crud
from app.crud import followup as followup_crud
from app.schemas.user import User
from datetime import datetime, timedelta
from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    """分析概览模型"""
    total_patients: int
    total_reports: int
    total_followups: int
    completion_rate: float
    average_age: float
    risk_distribution: Dict[str, int]


router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取分析概览"""
    # 获取基础统计数据
    patients = patient_crud.get_patients(db=db, user_id=current_user.id, limit=10000)
    reports = report_crud.get_reports(db=db, user_id=current_user.id, limit=10000)
    followups = followup_crud.get_followups(db=db, user_id=current_user.id, limit=10000)
    
    # 计算完成率
    completed_followups = len([f for f in followups if f.status.value == "completed"])
    completion_rate = (completed_followups / len(followups)) * 100 if followups else 0
    
    # 计算平均年龄
    total_age = sum(p.age for p in patients if p.age)
    average_age = total_age / len([p for p in patients if p.age]) if patients else 0
    
    # 风险分布
    risk_distribution = {}
    for patient in patients:
        risk_level = patient.risk_level.value if patient.risk_level else "未知"
        risk_distribution[risk_level] = risk_distribution.get(risk_level, 0) + 1
    
    return AnalyticsOverview(
        total_patients=len(patients),
        total_reports=len(reports),
        total_followups=len(followups),
        completion_rate=round(completion_rate, 2),
        average_age=round(average_age, 1),
        risk_distribution=risk_distribution
    )


@router.get("/risk-analysis")
def get_risk_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取风险分析"""
    patients = patient_crud.get_patients(db=db, user_id=current_user.id, limit=10000)
    
    risk_analysis = []
    risk_levels = ["low", "medium", "high", "critical"]
    
    for risk_level in risk_levels:
        risk_patients = [p for p in patients if p.risk_level and p.risk_level.value == risk_level]
        
        if risk_patients:
            # 计算平均年龄
            total_age = sum(p.age for p in risk_patients if p.age)
            average_age = total_age / len([p for p in risk_patients if p.age]) if risk_patients else 0
            
            # 性别分布
            gender_distribution = {}
            for patient in risk_patients:
                gender = patient.gender.value if patient.gender else "未知"
                gender_distribution[gender] = gender_distribution.get(gender, 0) + 1
            
            # 计算百分比
            percentage = (len(risk_patients) / len(patients)) * 100 if patients else 0
            
            risk_analysis.append({
                "risk_level": risk_level,
                "patient_count": len(risk_patients),
                "percentage": round(percentage, 2),
                "average_age": round(average_age, 1),
                "gender_distribution": gender_distribution
            })
    
    return risk_analysis


@router.get("/performance-metrics")
def get_performance_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取性能指标"""
    patients = patient_crud.get_patients(db=db, user_id=current_user.id, limit=10000)
    reports = report_crud.get_reports(db=db, user_id=current_user.id, limit=10000)
    followups = followup_crud.get_followups(db=db, user_id=current_user.id, limit=10000)
    
    # 计算各种指标
    total_patients = len(patients)
    total_reports = len(reports)
    total_followups = len(followups)
    
    # 完成率
    completed_followups = len([f for f in followups if f.status.value == "completed"])
    completion_rate = (completed_followups / total_followups) * 100 if total_followups > 0 else 0
    
    # 平均处理时间
    processing_times = []
    for report in reports:
        if report.processing_start_time and report.processing_end_time:
            processing_time = (report.processing_end_time - report.processing_start_time).total_seconds()
            processing_times.append(processing_time)
    
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    return {
        "total_patients": total_patients,
        "total_reports": total_reports,
        "total_followups": total_followups,
        "completion_rate": round(completion_rate, 2),
        "average_processing_time": round(avg_processing_time, 2)
    } 