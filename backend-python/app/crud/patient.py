from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.core.security import get_password_hash


def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    """根据ID获取患者信息"""
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_patient_id(db: Session, patient_id: str) -> Optional[Patient]:
    """根据患者编号获取患者信息"""
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()


def get_patient_by_user_id(db: Session, user_id: int) -> Optional[Patient]:
    """根据用户ID获取患者信息"""
    return db.query(Patient).filter(Patient.user_id == user_id).first()


def get_patients(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None,
    search: Optional[str] = None,
    risk_level: Optional[str] = None
) -> List[Patient]:
    """获取患者列表，支持分页、搜索和筛选"""
    query = db.query(Patient)
    
    # 按用户ID筛选
    if user_id:
        query = query.filter(Patient.user_id == user_id)
    
    # 搜索功能
    if search:
        search_filter = or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.patient_id.ilike(f"%{search}%"),
            Patient.phone.ilike(f"%{search}%"),
            Patient.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # 按风险等级筛选
    if risk_level:
        query = query.filter(Patient.risk_level == risk_level)
    
    return query.offset(skip).limit(limit).all()


def create_patient(db: Session, patient: PatientCreate, user_id: int) -> Patient:
    """创建新患者"""
    db_patient = Patient(
        **patient.dict(),
        user_id=user_id
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: int, patient: PatientUpdate) -> Optional[Patient]:
    """更新患者信息"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    update_data = patient.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int) -> bool:
    """删除患者"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return False
    
    db.delete(db_patient)
    db.commit()
    return True


def get_patients_by_risk_level(db: Session, risk_level: str, user_id: Optional[int] = None) -> List[Patient]:
    """根据风险等级获取患者列表"""
    query = db.query(Patient).filter(Patient.risk_level == risk_level)
    if user_id:
        query = query.filter(Patient.user_id == user_id)
    return query.all()


def get_patients_by_name(db: Session, name: str, limit: int = 100) -> List[Patient]:
    """根据患者姓名获取患者列表（支持多个档案编号）"""
    return db.query(Patient).filter(Patient.name == name).limit(limit).all()


def get_patients_count(
    db: Session, 
    user_id: Optional[int] = None,
    search: Optional[str] = None,
    risk_level: Optional[str] = None
) -> int:
    """获取患者总数，支持搜索和筛选"""
    query = db.query(Patient)
    
    # 按用户ID筛选
    if user_id:
        query = query.filter(Patient.user_id == user_id)
    
    # 搜索功能
    if search:
        search_filter = or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.patient_id.ilike(f"%{search}%"),
            Patient.phone.ilike(f"%{search}%"),
            Patient.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # 按风险等级筛选
    if risk_level:
        query = query.filter(Patient.risk_level == risk_level)
    
    return query.count()


def get_all_patients(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    risk_level: Optional[str] = None
) -> List[Patient]:
    """获取所有患者列表（机构客户使用），支持分页、搜索和筛选"""
    query = db.query(Patient)
    
    # 搜索功能
    if search:
        search_filter = or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.patient_id.ilike(f"%{search}%"),
            Patient.phone.ilike(f"%{search}%"),
            Patient.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # 按风险等级筛选
    if risk_level:
        query = query.filter(Patient.risk_level == risk_level)
    
    return query.offset(skip).limit(limit).all()


def get_all_patients_count(
    db: Session, 
    search: Optional[str] = None,
    risk_level: Optional[str] = None
) -> int:
    """获取所有患者总数（机构客户使用）"""
    query = db.query(Patient)
    
    # 搜索功能
    if search:
        search_filter = or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.patient_id.ilike(f"%{search}%"),
            Patient.phone.ilike(f"%{search}%"),
            Patient.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # 按风险等级筛选
    if risk_level:
        query = query.filter(Patient.risk_level == risk_level)
    
    return query.count()


def get_patients_by_age_range(db: Session, min_age: int, max_age: int, user_id: Optional[int] = None) -> List[Patient]:
    """根据年龄范围获取患者列表"""
    query = db.query(Patient).filter(
        and_(Patient.age >= min_age, Patient.age <= max_age)
    )
    if user_id:
        query = query.filter(Patient.user_id == user_id)
    return query.all()


def update_patient_risk_assessment(db: Session, patient_id: int, t_score: float, z_score: float, risk_level: str) -> Optional[Patient]:
    """更新患者风险评估"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    db_patient.t_score = t_score
    db_patient.z_score = z_score
    db_patient.risk_level = risk_level
    
    db.commit()
    db.refresh(db_patient)
    return db_patient 