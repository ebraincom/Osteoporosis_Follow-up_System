from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_dependency
from app.schemas.followup_response import (
    FollowupResponse,
    FollowupResponseCreate,
    FollowupResponseUpdate,
    FollowupResponseList,
    FollowupResponseWithPatient
)
from app.crud import followup_response as response_crud
from app.models.user import User

router = APIRouter()


def get_user_type(current_user: User) -> str:
    """获取用户类型"""
    if hasattr(current_user, 'user_type'):
        return current_user.user_type.lower()
    elif hasattr(current_user, '__class__') and 'PersonalUser' in str(current_user.__class__):
        return 'personal'
    else:
        return 'institutional'


@router.post("/", response_model=FollowupResponse)
def create_followup_response(
    response_data: FollowupResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """创建随访应答"""
    # 个人用户只能为自己创建应答
    if get_user_type(current_user) == "personal":
        # 根据followup_id找到对应的随访记录，获取patient_id
        from app.crud import followup as followup_crud
        followup = followup_crud.get_followup_record(db, followup_id=response_data.followup_id)
        
        if not followup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="随访记录不存在"
            )
        
        # 检查权限：个人用户只能回复自己的随访记录
        from app.crud import patient as patient_crud
        patient = patient_crud.get_patient(db, patient_id=followup.patient_id)
        
        if not patient or patient.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限回复此随访记录"
            )
        
        patient_id = followup.patient_id
    else:
        # 机构用户需要指定patient_id
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="机构用户不能直接创建随访应答"
        )
    
    return response_crud.create_followup_response(db, response_data, patient_id)


@router.get("/", response_model=FollowupResponseList)
def get_followup_responses(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    patient_id: Optional[int] = Query(None, description="患者ID筛选"),
    followup_id: Optional[int] = Query(None, description="随访记录ID筛选"),
    is_completed: Optional[bool] = Query(None, description="是否完成筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取随访应答列表"""
    # 根据用户类型决定查询范围
    if get_user_type(current_user) == "institutional":
        # 机构用户可以看到所有患者的应答
        responses = response_crud.get_followup_responses(
            db=db,
            skip=skip,
            limit=limit,
            patient_id=patient_id,
            followup_id=followup_id,
            is_completed=is_completed
        )
        total = response_crud.get_followup_responses_count(
            db=db,
            patient_id=patient_id,
            followup_id=followup_id,
            is_completed=is_completed
        )
    else:
        # 个人用户只能看到自己的应答
        # 根据患者姓名查询所有档案编号的随访回复
        responses = response_crud.get_followup_responses_by_patient_name(
            db=db,
            patient_name=current_user.name,
            skip=skip,
            limit=limit,
            followup_id=followup_id,
            is_completed=is_completed
        )
        total = response_crud.get_followup_responses_count_by_patient_name(
            db=db,
            patient_name=current_user.name,
            followup_id=followup_id,
            is_completed=is_completed
        )
    
    return FollowupResponseList(
        responses=responses,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/with-patient-info", response_model=List[dict])
def get_followup_responses_with_patient_info(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    patient_id: Optional[int] = Query(None, description="患者ID筛选"),
    is_completed: Optional[bool] = Query(None, description="是否完成筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取包含患者信息的随访应答列表（机构用户专用）"""
    if get_user_type(current_user) != "institutional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有机构用户才能查看患者信息"
        )
    
    responses = response_crud.get_followup_responses_with_patient_info(
        db=db,
        skip=skip,
        limit=limit,
        patient_id=patient_id,
        is_completed=is_completed
    )
    
    return responses


@router.get("/pending", response_model=List[dict])
def get_pending_followup_responses(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取待回复的随访记录（个人用户专用）"""
    # 检查用户类型
    user_type = getattr(current_user, 'user_type', 'personal')
    if hasattr(current_user, '__class__') and 'PersonalUser' in str(current_user.__class__):
        user_type = 'personal'
    
    if user_type != "personal":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有个人用户才能查看待回复的随访记录"
        )
    
    # 获取个人用户对应的患者记录（按姓名查询，支持多个档案编号）
    from app.crud import patient as patient_crud
    patients = patient_crud.get_patients_by_name(db, current_user.name, limit=1000)
    
    if not patients:
        return []
    
    # 获取所有患者ID
    patient_ids = [patient.id for patient in patients]
    
    pending_responses = response_crud.get_pending_followup_responses_for_patients(
        db=db,
        patient_ids=patient_ids,
        skip=skip,
        limit=limit
    )
    
    return pending_responses


@router.get("/{response_id}", response_model=FollowupResponse)
def get_followup_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取单个随访应答"""
    response = response_crud.get_followup_response(db, response_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访应答不存在"
        )
    
    # 检查权限
    if get_user_type(current_user) == "personal" and response.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限查看此随访应答"
        )
    
    return response


@router.put("/{response_id}", response_model=FollowupResponse)
def update_followup_response(
    response_id: int,
    response_update: FollowupResponseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """更新随访应答"""
    # 检查应答是否存在
    existing_response = response_crud.get_followup_response(db, response_id)
    if not existing_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访应答不存在"
        )
    
    # 检查权限
    if get_user_type(current_user) == "personal" and existing_response.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此随访应答"
        )
    
    updated_response = response_crud.update_followup_response(db, response_id, response_update)
    if not updated_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访应答不存在"
        )
    
    return updated_response


@router.delete("/{response_id}")
def delete_followup_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """删除随访应答"""
    # 检查应答是否存在
    existing_response = response_crud.get_followup_response(db, response_id)
    if not existing_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访应答不存在"
        )
    
    # 检查权限
    if get_user_type(current_user) == "personal" and existing_response.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此随访应答"
        )
    
    success = response_crud.delete_followup_response(db, response_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访应答不存在"
        )
    
    return {"message": "随访应答删除成功"}


@router.get("/patient/{patient_id}", response_model=List[FollowupResponse])
def get_patient_followup_responses(
    patient_id: int,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取指定患者的随访应答列表"""
    # 检查权限
    if get_user_type(current_user) == "personal":
        # 个人用户只能查看自己的患者记录的随访应答
        from app.crud import patient as patient_crud
        patient = patient_crud.get_patient(db, patient_id=patient_id)
        if not patient or patient.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限查看其他患者的随访应答"
            )
    
    responses = response_crud.get_patient_followup_responses(
        db=db,
        patient_id=patient_id,
        skip=skip,
        limit=limit
    )
    
    return responses