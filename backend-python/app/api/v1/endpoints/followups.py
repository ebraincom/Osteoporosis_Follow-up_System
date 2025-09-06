from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
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
    """获取当前用户的随访记录列表"""
    return followup_crud.get_user_followup_records(db, current_user.id, skip, limit)


@router.get("/my-records", response_model=List[Dict[str, Any]])
def get_my_patient_followup_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取个人用户作为患者的随访记录列表"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"=== my-records端点开始 ===")
    logger.info(f"当前用户: {current_user.username}, ID: {current_user.id}, 类型: {current_user.user_type}")
    logger.info(f"查询参数: skip={skip}, limit={limit}")
    
    # 个人用户需要获取与自己相关的所有随访记录
    # 通过患者姓名匹配来查找
    try:
        results = followup_crud.get_patient_followup_records_by_name(
            db, 
            patient_name=current_user.name, 
            skip=skip, 
            limit=limit
        )
        
        logger.info(f"查询结果类型: {type(results)}")
        logger.info(f"查询结果: {results}")
        
        if results:
            logger.info(f"找到 {len(results)} 条随访记录")
        else:
            logger.info("没有找到随访记录")
            
        return results
        
    except Exception as e:
        logger.error(f"查询随访记录时出错: {e}")
        import traceback
        logger.error(f"错误详情: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询随访记录失败: {str(e)}"
        )


@router.get("/all", response_model=List[FollowupRecord])
def get_all_followup_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取所有随访记录（机构用户使用）"""
    # 检查用户权限
    if current_user.user_type != "INSTITUTIONAL":
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
    
    # 检查权限：个人用户只能查看与自己相关的随访记录
    if current_user.user_type == "PERSONAL":
        # 通过患者姓名检查是否相关
        patient = followup_crud.get_patient_by_id(db, followup.patient_id)
        if not patient or patient.name != current_user.name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限访问此随访记录"
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
    # 检查权限：只有创建者或机构用户才能更新
    followup = followup_crud.get_followup_record(db, followup_id)
    if not followup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访记录不存在"
        )
    
    if followup.user_id != current_user.id and current_user.user_type != "INSTITUTIONAL":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此随访记录"
        )
    
    return followup_crud.update_followup_record(db, followup_id, followup_data)


@router.delete("/{followup_id}")
def delete_followup_record(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """删除随访记录"""
    # 检查权限：只有创建者或机构用户才能删除
    followup = followup_crud.get_followup_record(db, followup_id)
    if not followup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访记录不存在"
        )
    
    if followup.user_id != current_user.id and current_user.user_type != "INSTITUTIONAL":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此随访记录"
        )
    
    success = followup_crud.delete_followup_record(db, followup_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="随访记录不存在"
        )
    
    return {"message": "随访记录删除成功"} 