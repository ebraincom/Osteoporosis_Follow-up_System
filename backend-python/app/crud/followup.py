from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from app.models.followup import FollowupRecord
from app.models.patient import Patient
from app.models.user import User
from app.schemas.followup import FollowupRecordCreate, FollowupRecordUpdate
from datetime import datetime, timedelta


def create_followup_record(db: Session, followup_data: FollowupRecordCreate, user_id: int) -> FollowupRecord:
    """创建新的随访记录"""
    db_followup = FollowupRecord(
        **followup_data.dict(),
        user_id=user_id
    )
    db.add(db_followup)
    db.commit()
    db.refresh(db_followup)
    return db_followup


def get_followup_record(db: Session, followup_id: int) -> Optional[FollowupRecord]:
    """根据ID获取随访记录"""
    return db.query(FollowupRecord).filter(FollowupRecord.id == followup_id).first()


def get_patient_followup_records(
    db: Session, 
    patient_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[FollowupRecord]:
    """获取指定患者的随访记录列表"""
    return db.query(FollowupRecord)\
        .filter(FollowupRecord.patient_id == patient_id)\
        .order_by(desc(FollowupRecord.time))\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_patient_followup_records_by_name(
    db: Session, 
    patient_name: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[Dict[str, Any]]:
    """根据患者姓名获取随访记录列表，包含患者和医生信息"""
    results = db.query(
        FollowupRecord,
        Patient.name.label('patient_name'),
        Patient.patient_id.label('patient_patient_id'),
        User.name.label('doctor_name')
    )\
        .join(Patient, FollowupRecord.patient_id == Patient.id)\
        .join(User, FollowupRecord.user_id == User.id)\
        .filter(Patient.name == patient_name)\
        .order_by(desc(FollowupRecord.time))\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # 转换为字典格式
    followup_records = []
    for result in results:
        followup_dict = {
            'id': result.FollowupRecord.id,
            'patient_id': result.FollowupRecord.patient_id,
            'user_id': result.FollowupRecord.user_id,
            'time': result.FollowupRecord.time,
            'method': result.FollowupRecord.method,
            'location': result.FollowupRecord.location,
            'details': result.FollowupRecord.details,
            'notes': result.FollowupRecord.notes,
            'patient_status': result.FollowupRecord.patient_status,
            'next_followup_date': result.FollowupRecord.next_followup_date,
            'recommendations': result.FollowupRecord.recommendations,
            'created_at': result.FollowupRecord.created_at,
            'updated_at': result.FollowupRecord.updated_at,
            'patient_name': result.patient_name,
            'patient_patient_id': result.patient_patient_id,
            'doctor_name': result.doctor_name
        }
        followup_records.append(followup_dict)
    
    return followup_records


def get_user_followup_records(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[FollowupRecord]:
    """获取指定用户创建的随访记录列表"""
    return db.query(FollowupRecord)\
        .filter(FollowupRecord.user_id == user_id)\
        .order_by(desc(FollowupRecord.time))\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_all_followup_records(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[FollowupRecord]:
    """获取所有随访记录（机构用户使用）"""
    return db.query(FollowupRecord)\
        .order_by(desc(FollowupRecord.time))\
        .offset(skip)\
        .limit(limit)\
        .all()


def update_followup_record(
    db: Session, 
    followup_id: int, 
    followup_data: FollowupRecordUpdate
) -> Optional[FollowupRecord]:
    """更新随访记录"""
    db_followup = get_followup_record(db, followup_id)
    if not db_followup:
        return None
    
    update_data = followup_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_followup, field, value)
    
    db.commit()
    db.refresh(db_followup)
    return db_followup


def delete_followup_record(db: Session, followup_id: int) -> bool:
    """删除随访记录"""
    db_followup = get_followup_record(db, followup_id)
    if not db_followup:
        return False
    
    db.delete(db_followup)
    db.commit()
    return True


def get_patient_followup_count(db: Session, patient_id: int) -> int:
    """获取指定患者的随访记录数量"""
    return db.query(FollowupRecord).filter(FollowupRecord.patient_id == patient_id).count()


def get_latest_followup_record(db: Session, patient_id: int) -> Optional[FollowupRecord]:
    """获取指定患者的最新随访记录"""
    return db.query(FollowupRecord)\
        .filter(FollowupRecord.patient_id == patient_id)\
        .order_by(desc(FollowupRecord.time))\
        .first()


def get_patient_by_id(db: Session, patient_id: int) -> Optional[Patient]:
    """根据ID获取患者信息"""
    return db.query(Patient).filter(Patient.id == patient_id).first() 