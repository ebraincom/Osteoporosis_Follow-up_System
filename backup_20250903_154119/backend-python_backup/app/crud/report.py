from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate
from datetime import datetime


def get_report(db: Session, report_id: int) -> Optional[Report]:
    """根据ID获取报告"""
    return db.query(Report).filter(Report.id == report_id).first()


def get_report_by_report_id(db: Session, report_id: str) -> Optional[Report]:
    """根据报告编号获取报告"""
    return db.query(Report).filter(Report.report_id == report_id).first()


def get_reports(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    report_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Report]:
    """获取报告列表，支持分页、搜索和筛选"""
    query = db.query(Report)
    
    # 按用户ID筛选
    if user_id:
        query = query.filter(Report.user_id == user_id)
    
    # 按患者ID筛选
    if patient_id:
        query = query.filter(Report.patient_id == patient_id)
    
    # 按报告类型筛选
    if report_type:
        query = query.filter(Report.report_type == report_type)
    
    # 按状态筛选
    if status:
        query = query.filter(Report.status == status)
    
    # 搜索功能
    if search:
        search_filter = or_(
            Report.title.ilike(f"%{search}%"),
            Report.report_id.ilike(f"%{search}%"),
            Report.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.order_by(desc(Report.created_at)).offset(skip).limit(limit).all()


def create_report(db: Session, report: ReportCreate, user_id: int) -> Report:
    """创建新报告"""
    db_report = Report(
        **report.dict(),
        user_id=user_id,
        processing_start_time=datetime.utcnow()
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def update_report(db: Session, report_id: int, report: ReportUpdate) -> Optional[Report]:
    """更新报告信息"""
    db_report = get_report(db, report_id)
    if not db_report:
        return None
    
    update_data = report.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_report, field, value)
    
    db.commit()
    db.refresh(db_report)
    return db_report


def delete_report(db: Session, report_id: int) -> bool:
    """删除报告"""
    db_report = get_report(db, report_id)
    if not db_report:
        return False
    
    db.delete(db_report)
    db.commit()
    return True


def get_reports_by_patient(db: Session, patient_id: int, user_id: Optional[int] = None) -> List[Report]:
    """获取患者的所有报告"""
    query = db.query(Report).filter(Report.patient_id == patient_id)
    if user_id:
        query = query.filter(Report.user_id == user_id)
    return query.order_by(desc(Report.created_at)).all()


def get_reports_by_type(db: Session, report_type: str, user_id: Optional[int] = None) -> List[Report]:
    """根据报告类型获取报告列表"""
    query = db.query(Report).filter(Report.report_type == report_type)
    if user_id:
        query = query.filter(Report.user_id == user_id)
    return query.order_by(desc(Report.created_at)).all()


def get_reports_by_status(db: Session, status: str, user_id: Optional[int] = None) -> List[Report]:
    """根据状态获取报告列表"""
    query = db.query(Report).filter(Report.status == status)
    if user_id:
        query = query.filter(Report.user_id == user_id)
    return query.order_by(desc(Report.created_at)).all()


def update_report_status(db: Session, report_id: int, status: str) -> Optional[Report]:
    """更新报告状态"""
    db_report = get_report(db, report_id)
    if not db_report:
        return None
    
    db_report.status = status
    if status == "completed":
        db_report.processing_end_time = datetime.utcnow()
    
    db.commit()
    db.refresh(db_report)
    return db_report


def update_ai_analysis(db: Session, report_id: int, ai_analysis: str, ai_recommendations: str) -> Optional[Report]:
    """更新AI分析结果"""
    db_report = get_report(db, report_id)
    if not db_report:
        return None
    
    db_report.ai_analysis = ai_analysis
    db_report.ai_recommendations = ai_recommendations
    db_report.status = "completed"
    db_report.processing_end_time = datetime.utcnow()
    
    db.commit()
    db.refresh(db_report)
    return db_report


def get_reports_count(db: Session, user_id: Optional[int] = None) -> int:
    """获取报告总数"""
    query = db.query(Report)
    if user_id:
        query = query.filter(Report.user_id == user_id)
    return query.count()


def get_reports_statistics(db: Session, user_id: Optional[int] = None) -> dict:
    """获取报告统计信息"""
    query = db.query(Report)
    if user_id:
        query = query.filter(Report.user_id == user_id)
    
    reports = query.all()
    
    # 按类型统计
    type_stats = {}
    for report in reports:
        report_type = report.report_type.value if report.report_type else "未知"
        type_stats[report_type] = type_stats.get(report_type, 0) + 1
    
    # 按状态统计
    status_stats = {}
    for report in reports:
        status = report.status.value if report.status else "未知"
        status_stats[status] = status_stats.get(status, 0) + 1
    
    # 计算平均处理时间
    processing_times = []
    for report in reports:
        if report.processing_start_time and report.processing_end_time:
            processing_time = (report.processing_end_time - report.processing_start_time).total_seconds()
            processing_times.append(processing_time)
    
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    return {
        "total_reports": len(reports),
        "reports_by_type": type_stats,
        "reports_by_status": status_stats,
        "average_processing_time": round(avg_processing_time, 2)
    } 