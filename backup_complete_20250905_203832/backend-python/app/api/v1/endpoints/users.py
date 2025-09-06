from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user
from app.crud import user as user_crud
from app.schemas.user import User, UserUpdate

router = APIRouter()


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户信息"""
    return current_user


@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新当前用户信息"""
    # 不允许更新用户名和邮箱
    if user_update.username or user_update.email:
        raise HTTPException(status_code=400, detail="不能修改用户名和邮箱")
    
    updated_user = user_crud.update_user(db=db, user_id=current_user.id, user=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return updated_user


@router.get("/statistics/overview")
def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取用户统计信息（仅管理员）"""
    # 检查权限：只有管理员可以查看用户统计
    if current_user.user_type.value != "institutional":
        raise HTTPException(status_code=403, detail="没有权限查看用户统计")
    
    users = user_crud.get_users(db=db, limit=10000)
    
    # 按用户类型统计
    type_stats = {}
    for user in users:
        user_type = user.user_type.value if user.user_type else "未知"
        type_stats[user_type] = type_stats.get(user_type, 0) + 1
    
    # 按状态统计
    status_stats = {
        "active": len([u for u in users if u.is_active]),
        "inactive": len([u for u in users if not u.is_active])
    }
    
    return {
        "total_users": len(users),
        "users_by_type": type_stats,
        "users_by_status": status_stats
    } 