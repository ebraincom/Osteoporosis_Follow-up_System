from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_dependency
from app.crud import patient as patient_crud
from app.schemas.patient import Patient, PatientCreate, PatientUpdate, PatientList, PatientStatistics
from app.schemas.user import User, UserType

router = APIRouter()


@router.get("/", response_model=PatientList)
def get_patients(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    risk_level: Optional[str] = Query(None, description="风险等级筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取患者列表"""
    # 根据用户类型决定查询范围
    if current_user.user_type == UserType.INSTITUTIONAL:
        # 机构客户（医生）可以查看所有患者信息
        patients = patient_crud.get_all_patients(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            risk_level=risk_level
        )
        total = patient_crud.get_all_patients_count(
            db=db, 
            search=search, 
            risk_level=risk_level
        )
    else:
        # 个人用户只能查看自己的患者信息
        patients = patient_crud.get_patients(
            db=db,
            skip=skip,
            limit=limit,
            user_id=current_user.id,
            search=search,
            risk_level=risk_level
        )
        total = patient_crud.get_patients_count(
            db=db, 
            user_id=current_user.id,
            search=search, 
            risk_level=risk_level
        )
    
    return PatientList(
        patients=patients,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{patient_id}", response_model=Patient)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取单个患者信息"""
    patient = patient_crud.get_patient(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    # 检查权限：只能查看自己的患者
    if patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限访问此患者信息")
    
    return patient


@router.post("/", response_model=Patient)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """创建新患者"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"=== 开始创建患者 ===")
    logger.info(f"患者姓名: {patient.name}")
    logger.info(f"患者编号: {patient.patient_id}")
    logger.info(f"当前用户: {current_user.username} (ID: {current_user.id})")
    logger.info(f"请求数据: {patient.dict()}")
    
    # 检查患者编号是否已存在
    existing_patient = patient_crud.get_patient_by_patient_id(db, patient.patient_id)
    if existing_patient:
        logger.warning(f"患者编号已存在: {patient.patient_id}")
        raise HTTPException(status_code=400, detail="患者编号已存在")
    
    try:
        result = patient_crud.create_patient(db=db, patient=patient, user_id=current_user.id)
        logger.info(f"患者创建成功: {result.id}")
        logger.info(f"=== 患者创建完成 ===")
        return result
    except Exception as e:
        logger.error(f"患者创建失败: {e}")
        logger.error(f"错误详情: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建患者失败: {str(e)}")


@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """更新患者信息"""
    # 检查患者是否存在
    existing_patient = patient_crud.get_patient(db, patient_id=patient_id)
    if not existing_patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    # 检查权限
    if existing_patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此患者信息")
    
    # 如果更新患者编号，检查是否与其他患者冲突
    if patient.patient_id and patient.patient_id != existing_patient.patient_id:
        conflict_patient = patient_crud.get_patient_by_patient_id(db, patient.patient_id)
        if conflict_patient:
            raise HTTPException(status_code=400, detail="患者编号已存在")
    
    updated_patient = patient_crud.update_patient(db=db, patient_id=patient_id, patient=patient)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    return updated_patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """删除患者"""
    # 检查患者是否存在
    existing_patient = patient_crud.get_patient(db, patient_id=patient_id)
    if not existing_patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    # 检查权限：只能删除自己的患者
    if existing_patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除此患者信息")
    
    success = patient_crud.delete_patient(db=db, patient_id=patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    return {"message": "患者删除成功"}


@router.get("/risk-level/{risk_level}", response_model=List[Patient])
def get_patients_by_risk_level(
    risk_level: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """根据风险等级获取患者列表"""
    patients = patient_crud.get_patients_by_risk_level(
        db=db, 
        risk_level=risk_level, 
        user_id=current_user.id
    )
    return patients


@router.get("/statistics/overview", response_model=PatientStatistics)
def get_patient_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取患者统计信息"""
    # 获取所有患者
    patients = patient_crud.get_patients(db=db, user_id=current_user.id, limit=10000)
    
    if not patients:
        return PatientStatistics(
            total_patients=0,
            patients_by_risk_level={},
            patients_by_age_group={},
            patients_by_gender={},
            average_age=0
        )
    
    # 按风险等级统计
    risk_level_stats = {}
    for patient in patients:
        risk_level = patient.risk_level.value if patient.risk_level else "未知"
        risk_level_stats[risk_level] = risk_level_stats.get(risk_level, 0) + 1
    
    # 按年龄组统计
    age_group_stats = {}
    for patient in patients:
        if patient.age < 30:
            age_group = "30岁以下"
        elif patient.age < 50:
            age_group = "30-50岁"
        elif patient.age < 70:
            age_group = "50-70岁"
        else:
            age_group = "70岁以上"
        age_group_stats[age_group] = age_group_stats.get(age_group, 0) + 1
    
    # 按性别统计
    gender_stats = {}
    for patient in patients:
        gender = patient.gender.value if patient.gender else "未知"
        gender_stats[gender] = gender_stats.get(gender, 0) + 1
    
    # 计算平均值
    total_age = sum(p.age for p in patients if p.age)
    average_age = total_age / len([p for p in patients if p.age]) if patients else 0
    
    total_bmi = sum(p.bmi for p in patients if p.bmi)
    average_bmi = total_bmi / len([p for p in patients if p.bmi]) if any(p.bmi for p in patients) else None
    
    total_t_score = sum(p.t_score for p in patients if p.t_score)
    average_t_score = total_t_score / len([p for p in patients if p.t_score]) if any(p.t_score for p in patients) else None
    
    total_z_score = sum(p.z_score for p in patients if p.z_score)
    average_z_score = total_z_score / len([p for p in patients if p.z_score]) if any(p.z_score for p in patients) else None
    
    return PatientStatistics(
        total_patients=len(patients),
        patients_by_risk_level=risk_level_stats,
        patients_by_age_group=age_group_stats,
        patients_by_gender=gender_stats,
        average_age=round(average_age, 1),
        average_bmi=round(average_bmi, 1) if average_bmi else None,
        average_t_score=round(average_t_score, 2) if average_t_score else None,
        average_z_score=round(average_z_score, 2) if average_z_score else None
    )


@router.put("/{patient_id}/risk-assessment")
def update_risk_assessment(
    patient_id: int,
    t_score: float,
    z_score: float,
    risk_level: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """更新患者风险评估"""
    # 检查患者是否存在
    existing_patient = patient_crud.get_patient(db, patient_id=patient_id)
    if not existing_patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    # 检查权限
    if existing_patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此患者信息")
    
    updated_patient = patient_crud.update_patient_risk_assessment(
        db=db, 
        patient_id=patient_id, 
        t_score=t_score, 
        z_score=z_score, 
        risk_level=risk_level
    )
    
    if not updated_patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    return {"message": "风险评估更新成功", "patient": updated_patient} 