from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.followup_response import FollowupResponse
from app.models.followup import FollowupRecord
from app.models.patient import Patient
from app.schemas.followup_response import FollowupResponseCreate, FollowupResponseUpdate


def create_followup_response(db: Session, response_data: FollowupResponseCreate, patient_id: int) -> FollowupResponse:
    """创建随访应答"""
    from datetime import datetime
    
    db_response = FollowupResponse(
        **response_data.dict(),
        patient_id=patient_id,
        response_time=datetime.now()  # 设置回复时间
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_followup_response(db: Session, response_id: int) -> Optional[FollowupResponse]:
    """获取单个随访应答"""
    return db.query(FollowupResponse).filter(FollowupResponse.id == response_id).first()


def get_followup_responses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    followup_id: Optional[int] = None,
    is_completed: Optional[bool] = None
) -> List[FollowupResponse]:
    """获取随访应答列表"""
    query = db.query(FollowupResponse)
    
    if patient_id is not None:
        query = query.filter(FollowupResponse.patient_id == patient_id)
    
    if followup_id is not None:
        query = query.filter(FollowupResponse.followup_id == followup_id)
    
    if is_completed is not None:
        query = query.filter(FollowupResponse.is_completed == is_completed)
    
    return query.offset(skip).limit(limit).all()


def get_followup_responses_count(
    db: Session,
    patient_id: Optional[int] = None,
    followup_id: Optional[int] = None,
    is_completed: Optional[bool] = None
) -> int:
    """获取随访应答总数"""
    query = db.query(FollowupResponse)
    
    if patient_id is not None:
        query = query.filter(FollowupResponse.patient_id == patient_id)
    
    if followup_id is not None:
        query = query.filter(FollowupResponse.followup_id == followup_id)
    
    if is_completed is not None:
        query = query.filter(FollowupResponse.is_completed == is_completed)
    
    return query.count()


def get_patient_followup_responses(
    db: Session,
    patient_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[FollowupResponse]:
    """获取指定患者的随访应答列表"""
    return db.query(FollowupResponse).filter(
        FollowupResponse.patient_id == patient_id
    ).offset(skip).limit(limit).all()


def get_followup_responses_with_patient_info(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    is_completed: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """获取包含患者信息的随访应答列表"""
    query = db.query(
        FollowupResponse,
        Patient.name.label('patient_name'),
        Patient.phone.label('patient_phone'),
        FollowupRecord.time.label('followup_time'),
        FollowupRecord.details.label('followup_details')
    ).join(
        Patient, FollowupResponse.patient_id == Patient.id
    ).join(
        FollowupRecord, FollowupResponse.followup_id == FollowupRecord.id
    )
    
    if patient_id is not None:
        query = query.filter(FollowupResponse.patient_id == patient_id)
    
    if is_completed is not None:
        query = query.filter(FollowupResponse.is_completed == is_completed)
    
    results = query.offset(skip).limit(limit).all()
    
    # 转换为字典格式
    response_list = []
    for result in results:
        response_dict = {
            'id': result.FollowupResponse.id,
            'followup_id': result.FollowupResponse.followup_id,
            'patient_id': result.FollowupResponse.patient_id,
            'response_time': result.FollowupResponse.response_time,
            'is_completed': result.FollowupResponse.is_completed,
            'overall_feeling': result.FollowupResponse.overall_feeling,
            'improvement_level': result.FollowupResponse.improvement_level,
            'medication_adherence': result.FollowupResponse.medication_adherence,
            'exercise_volume': result.FollowupResponse.exercise_volume,
            'diet_adjustment': result.FollowupResponse.diet_adjustment,
            'pain_level': result.FollowupResponse.pain_level,
            'sleep_quality': result.FollowupResponse.sleep_quality,
            'daily_activity': result.FollowupResponse.daily_activity,
            'mood_status': result.FollowupResponse.mood_status,
            'social_activity': result.FollowupResponse.social_activity,
            'side_effects': result.FollowupResponse.side_effects,
            'concerns': result.FollowupResponse.concerns,
            'suggestions': result.FollowupResponse.suggestions,
            'additional_info': result.FollowupResponse.additional_info,
            'created_at': result.FollowupResponse.created_at,
            'updated_at': result.FollowupResponse.updated_at,
            'patient_name': result.patient_name,
            'patient_phone': result.patient_phone,
            'followup_time': result.followup_time,
            'followup_details': result.followup_details
        }
        response_list.append(response_dict)
    
    return response_list


def update_followup_response(
    db: Session,
    response_id: int,
    response_update: FollowupResponseUpdate
) -> Optional[FollowupResponse]:
    """更新随访应答"""
    db_response = db.query(FollowupResponse).filter(FollowupResponse.id == response_id).first()
    if not db_response:
        return None
    
    update_data = response_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_response, field, value)
    
    db.commit()
    db.refresh(db_response)
    return db_response


def delete_followup_response(db: Session, response_id: int) -> bool:
    """删除随访应答"""
    db_response = db.query(FollowupResponse).filter(FollowupResponse.id == response_id).first()
    if not db_response:
        return False
    
    db.delete(db_response)
    db.commit()
    return True


def get_pending_followup_responses(
    db: Session,
    patient_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """获取患者待回复的随访记录"""
    # 查找有随访记录但还没有应答的记录
    query = db.query(
        FollowupRecord,
        Patient.name.label('patient_name'),
        Patient.phone.label('patient_phone')
    ).join(
        Patient, FollowupRecord.patient_id == Patient.id
    ).outerjoin(
        FollowupResponse, and_(
            FollowupResponse.followup_id == FollowupRecord.id,
            FollowupResponse.patient_id == patient_id
        )
    ).filter(
        and_(
            FollowupRecord.patient_id == patient_id,
            FollowupResponse.id.is_(None)  # 没有应答的记录
        )
    )
    
    results = query.offset(skip).limit(limit).all()
    
    # 转换为字典格式
    pending_list = []
    for result in results:
        pending_dict = {
            'followup_id': result.FollowupRecord.id,
            'patient_id': result.FollowupRecord.patient_id,
            'followup_time': result.FollowupRecord.time,
            'method': result.FollowupRecord.method,
            'location': result.FollowupRecord.location,
            'details': result.FollowupRecord.details,
            'patient_status': result.FollowupRecord.patient_status,
            'next_followup_date': result.FollowupRecord.next_followup_date,
            'recommendations': result.FollowupRecord.recommendations,
            'created_at': result.FollowupRecord.created_at,
            'patient_name': result.patient_name,
            'patient_phone': result.patient_phone
        }
        pending_list.append(pending_dict)
    
    return pending_list


def get_pending_followup_responses_for_patients(
    db: Session,
    patient_ids: List[int],
    skip: int = 0,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """获取多个患者待回复的随访记录"""
    if not patient_ids:
        return []
    
    # 查找有随访记录但还没有应答的记录
    query = db.query(
        FollowupRecord,
        Patient.name.label('patient_name'),
        Patient.phone.label('patient_phone')
    ).join(
        Patient, FollowupRecord.patient_id == Patient.id
    ).outerjoin(
        FollowupResponse, FollowupResponse.followup_id == FollowupRecord.id
    ).filter(
        and_(
            FollowupRecord.patient_id.in_(patient_ids),
            FollowupResponse.id.is_(None)  # 没有应答的记录
        )
    )
    
    results = query.offset(skip).limit(limit).all()
    
    # 转换为字典格式
    pending_list = []
    for result in results:
        pending_dict = {
            'followup_id': result.FollowupRecord.id,
            'patient_id': result.FollowupRecord.patient_id,
            'followup_time': result.FollowupRecord.time,
            'method': result.FollowupRecord.method,
            'location': result.FollowupRecord.location,
            'details': result.FollowupRecord.details,
            'patient_status': result.FollowupRecord.patient_status,
            'next_followup_date': result.FollowupRecord.next_followup_date,
            'recommendations': result.FollowupRecord.recommendations,
            'created_at': result.FollowupRecord.created_at,
            'patient_name': result.patient_name,
            'patient_phone': result.patient_phone
        }
        pending_list.append(pending_dict)
    
    return pending_list


def get_followup_responses_by_patient_name(
    db: Session,
    patient_name: str,
    skip: int = 0,
    limit: int = 100,
    followup_id: Optional[int] = None,
    is_completed: Optional[bool] = None
) -> List[FollowupResponse]:
    """根据患者姓名获取随访应答列表（支持多个档案编号）"""
    query = db.query(FollowupResponse).join(
        Patient, FollowupResponse.patient_id == Patient.id
    ).filter(Patient.name == patient_name)
    
    if followup_id is not None:
        query = query.filter(FollowupResponse.followup_id == followup_id)
    
    if is_completed is not None:
        query = query.filter(FollowupResponse.is_completed == is_completed)
    
    return query.offset(skip).limit(limit).all()


def get_followup_responses_count_by_patient_name(
    db: Session,
    patient_name: str,
    followup_id: Optional[int] = None,
    is_completed: Optional[bool] = None
) -> int:
    """根据患者姓名获取随访应答总数（支持多个档案编号）"""
    query = db.query(FollowupResponse).join(
        Patient, FollowupResponse.patient_id == Patient.id
    ).filter(Patient.name == patient_name)
    
    if followup_id is not None:
        query = query.filter(FollowupResponse.followup_id == followup_id)
    
    if is_completed is not None:
        query = query.filter(FollowupResponse.is_completed == is_completed)
    
    return query.count()


def get_followup_responses_with_patient_info_by_name(
    db: Session,
    patient_name: str,
    skip: int = 0,
    limit: int = 100,
    is_completed: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """根据患者姓名获取包含患者信息的随访应答列表（支持多个档案编号）"""
    query = db.query(
        FollowupResponse,
        Patient.name.label('patient_name'),
        Patient.patient_id.label('patient_patient_id'),
        Patient.phone.label('patient_phone'),
        FollowupRecord.time.label('followup_time'),
        FollowupRecord.details.label('followup_details')
    ).join(
        Patient, FollowupResponse.patient_id == Patient.id
    ).join(
        FollowupRecord, FollowupResponse.followup_id == FollowupRecord.id
    ).filter(Patient.name == patient_name)
    
    if is_completed is not None:
        query = query.filter(FollowupResponse.is_completed == is_completed)
    
    results = query.offset(skip).limit(limit).all()
    
    # 转换为字典格式
    response_list = []
    for result in results:
        response_dict = {
            'id': result.FollowupResponse.id,
            'followup_id': result.FollowupResponse.followup_id,
            'patient_id': result.FollowupResponse.patient_id,
            'response_time': result.FollowupResponse.response_time,
            'is_completed': result.FollowupResponse.is_completed,
            'overall_feeling': result.FollowupResponse.overall_feeling,
            'improvement_level': result.FollowupResponse.improvement_level,
            'medication_adherence': result.FollowupResponse.medication_adherence,
            'exercise_volume': result.FollowupResponse.exercise_volume,
            'diet_adjustment': result.FollowupResponse.diet_adjustment,
            'pain_level': result.FollowupResponse.pain_level,
            'sleep_quality': result.FollowupResponse.sleep_quality,
            'daily_activity': result.FollowupResponse.daily_activity,
            'mood_status': result.FollowupResponse.mood_status,
            'social_activity': result.FollowupResponse.social_activity,
            'side_effects': result.FollowupResponse.side_effects,
            'concerns': result.FollowupResponse.concerns,
            'suggestions': result.FollowupResponse.suggestions,
            'additional_info': result.FollowupResponse.additional_info,
            'created_at': result.FollowupResponse.created_at,
            'updated_at': result.FollowupResponse.updated_at,
            'patient_name': result.patient_name,
            'patient_patient_id': result.patient_patient_id,  # 档案编号
            'patient_phone': result.patient_phone,
            'followup_time': result.followup_time,
            'followup_details': result.followup_details
        }
        response_list.append(response_dict)
    
    return response_list