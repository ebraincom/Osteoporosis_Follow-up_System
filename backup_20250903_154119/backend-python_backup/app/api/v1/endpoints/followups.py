from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user_dependency
from app.schemas.followup import (
    FollowupRecord, 
    FollowupRecordCreate, 
    FollowupRecordUpdate,
    FollowupRecordWithPatient
)
from app.crud import followup as followup_crud
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=FollowupRecord)
def create_followup_record(
    followup_data: FollowupRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """创建随访记录"""
    return followup_crud.create_followup_record(db, followup_data, current_user.id)


@router.get("/patient/{patient_id}", response_model=List[FollowupRecord])
def get_patient_followup_records(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取指定患者的随访记录列表"""
    return followup_crud.get_patient_followup_records(db, patient_id, skip, limit)


@router.get("/user/me", response_model=List[FollowupRecord])
def get_my_followup_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取当前用户创建的随访记录列表"""
    return followup_crud.get_user_followup_records(db, current_user.id, skip, limit)


@router.get("/all", response_model=List[FollowupRecord])
def get_all_followup_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取所有随访记录（机构用户使用）"""
    if current_user.user_type.value != "institutional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有机构用户才能查看所有随访记录"
        )
    return followup_crud.get_all_followup_records(db, skip, limit)


@router.get("/{followup_id}", response_model=FollowupRecord)
def get_followup_record(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取随访记录详情"""
    followup = followup_crud.get_followup_record(db, followup_id)
    if not followup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访记录不存在"
        )
    return followup


@router.put("/{followup_id}", response_model=FollowupRecord)
def update_followup_record(
    followup_id: int,
    followup_data: FollowupRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """更新随访记录"""
    # 检查随访记录是否存在
    existing_followup = followup_crud.get_followup_record(db, followup_id)
    if not existing_followup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访记录不存在"
        )
    
    # 检查权限（只有创建者或机构用户才能编辑）
    if existing_followup.user_id != current_user.id and current_user.user_type.value != "institutional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限编辑此随访记录"
        )
    
    updated_followup = followup_crud.update_followup_record(db, followup_id, followup_data)
    if not updated_followup:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新随访记录失败"
        )
    return updated_followup


@router.delete("/{followup_id}")
def delete_followup_record(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """删除随访记录"""
    # 检查随访记录是否存在
    existing_followup = followup_crud.get_followup_record(db, followup_id)
    if not existing_followup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访记录不存在"
        )
    
    # 检查权限（只有创建者或机构用户才能删除）
    if existing_followup.user_id != current_user.id and current_user.user_type.value != "institutional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此随访记录"
        )
    
    success = followup_crud.delete_followup_record(db, followup_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除随访记录失败"
        )
    
    return {"message": "随访记录删除成功"} 