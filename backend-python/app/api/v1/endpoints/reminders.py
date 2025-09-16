from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.security import get_current_user_dependency
from app.models.user import User
from datetime import datetime, timedelta

router = APIRouter()


def get_user_type(current_user: User) -> str:
    """获取用户类型"""
    if hasattr(current_user, 'user_type'):
        return current_user.user_type.lower()
    elif hasattr(current_user, '__class__') and 'PersonalUser' in str(current_user.__class__):
        return 'personal'
    else:
        return 'institutional'


@router.get("/settings")
def get_reminder_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取用户的提醒设置"""
    try:
        # 确定用户类型
        user_type = get_user_type(current_user)
        
        result = db.execute(text("""
            SELECT * FROM reminder_settings 
            WHERE user_id = :user_id AND user_type = :user_type
        """), {"user_id": current_user.id, "user_type": user_type})
        
        settings = result.fetchone()
        
        if not settings:
            # 如果没有设置，返回默认设置
            default_settings = {
                "id": None,
                "user_id": current_user.id,
                "user_type": user_type,
                "is_enabled": True,
                "email_reminder": False,
                "sms_reminder": False,
                "app_reminder": True,
                "advance_days": 3,
                "reminder_time": "09:00",
                "urgent_reminder": True,
                "medication_reminder": True,
                "checkup_reminder": False,
                "birthday_reminder": False,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            return default_settings
        
        # 转换为字典格式
        columns = ['id', 'user_id', 'user_type', 'is_enabled', 'email_reminder', 'sms_reminder', 
                  'app_reminder', 'advance_days', 'reminder_time', 'urgent_reminder', 
                  'medication_reminder', 'checkup_reminder', 'birthday_reminder', 'created_at', 'updated_at']
        settings_dict = dict(zip(columns, settings))
        
        # 转换布尔值
        for key in ['is_enabled', 'email_reminder', 'sms_reminder', 'app_reminder', 
                   'urgent_reminder', 'medication_reminder', 'checkup_reminder', 'birthday_reminder']:
            if key in settings_dict:
                settings_dict[key] = bool(settings_dict[key])
        
        return settings_dict
        
    except Exception as e:
        print(f"获取提醒设置失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取提醒设置失败: {str(e)}"
        )


@router.put("/settings")
def update_reminder_settings(
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """更新用户的提醒设置"""
    try:
        # 确定用户类型
        user_type = get_user_type(current_user)
        
        # 检查是否存在设置记录
        result = db.execute(text("""
            SELECT id FROM reminder_settings 
            WHERE user_id = :user_id AND user_type = :user_type
        """), {"user_id": current_user.id, "user_type": user_type})
        
        existing = result.fetchone()
        
        if existing:
            # 更新现有设置
            db.execute(text("""
                UPDATE reminder_settings SET
                    is_enabled = :is_enabled, email_reminder = :email_reminder, sms_reminder = :sms_reminder, app_reminder = :app_reminder,
                    advance_days = :advance_days, reminder_time = :reminder_time, urgent_reminder = :urgent_reminder,
                    medication_reminder = :medication_reminder, checkup_reminder = :checkup_reminder, birthday_reminder = :birthday_reminder,
                    updated_at = :updated_at
                WHERE user_id = :user_id AND user_type = :user_type
            """), {
                "is_enabled": settings_data.get('is_enabled', True),
                "email_reminder": settings_data.get('email_reminder', False),
                "sms_reminder": settings_data.get('sms_reminder', False),
                "app_reminder": settings_data.get('app_reminder', True),
                "advance_days": settings_data.get('advance_days', 3),
                "reminder_time": settings_data.get('reminder_time', '09:00'),
                "urgent_reminder": settings_data.get('urgent_reminder', True),
                "medication_reminder": settings_data.get('medication_reminder', True),
                "checkup_reminder": settings_data.get('checkup_reminder', False),
                "birthday_reminder": settings_data.get('birthday_reminder', False),
                "updated_at": datetime.now().isoformat(),
                "user_id": current_user.id,
                "user_type": user_type
            })
        else:
            # 创建新设置
            db.execute(text("""
                INSERT INTO reminder_settings 
                (user_id, user_type, is_enabled, email_reminder, sms_reminder, app_reminder,
                 advance_days, reminder_time, urgent_reminder, medication_reminder,
                 checkup_reminder, birthday_reminder, created_at, updated_at)
                VALUES (:user_id, :user_type, :is_enabled, :email_reminder, :sms_reminder, :app_reminder,
                        :advance_days, :reminder_time, :urgent_reminder, :medication_reminder,
                        :checkup_reminder, :birthday_reminder, :created_at, :updated_at)
            """), {
                "user_id": current_user.id,
                "user_type": user_type,
                "is_enabled": settings_data.get('is_enabled', True),
                "email_reminder": settings_data.get('email_reminder', False),
                "sms_reminder": settings_data.get('sms_reminder', False),
                "app_reminder": settings_data.get('app_reminder', True),
                "advance_days": settings_data.get('advance_days', 3),
                "reminder_time": settings_data.get('reminder_time', '09:00'),
                "urgent_reminder": settings_data.get('urgent_reminder', True),
                "medication_reminder": settings_data.get('medication_reminder', True),
                "checkup_reminder": settings_data.get('checkup_reminder', False),
                "birthday_reminder": settings_data.get('birthday_reminder', False),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
        
        db.commit()
        return {"message": "提醒设置更新成功"}
        
    except Exception as e:
        print(f"更新提醒设置失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新提醒设置失败: {str(e)}"
        )


@router.get("/recent")
def get_recent_reminders(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取最近的提醒记录"""
    try:
        user_type = get_user_type(current_user)
        
        result = db.execute(text("""
            SELECT * FROM reminder_records 
            WHERE user_id = :user_id AND user_type = :user_type
            ORDER BY scheduled_time DESC
            LIMIT :limit
        """), {"user_id": current_user.id, "user_type": user_type, "limit": limit})
        
        reminders = result.fetchall()
        columns = ['id', 'user_id', 'user_type', 'reminder_type', 'title', 'content', 'scheduled_time',
                  'is_sent', 'sent_time', 'is_read', 'read_time', 'related_id', 'created_at', 'updated_at']
        
        reminder_list = []
        for reminder in reminders:
            reminder_dict = dict(zip(columns, reminder))
            # 转换布尔值
            for key in ['is_sent', 'is_read']:
                if key in reminder_dict:
                    reminder_dict[key] = bool(reminder_dict[key])
            reminder_list.append(reminder_dict)
        
        return reminder_list
        
    except Exception as e:
        print(f"获取最近提醒失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取最近提醒失败: {str(e)}"
        )


@router.get("/history")
def get_reminder_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """获取提醒历史记录"""
    try:
        user_type = get_user_type(current_user)
        
        result = db.execute(text("""
            SELECT * FROM reminder_records 
            WHERE user_id = :user_id AND user_type = :user_type
            ORDER BY scheduled_time DESC
            LIMIT :limit OFFSET :skip
        """), {"user_id": current_user.id, "user_type": user_type, "limit": limit, "skip": skip})
        
        reminders = result.fetchall()
        columns = ['id', 'user_id', 'user_type', 'reminder_type', 'title', 'content', 'scheduled_time',
                  'is_sent', 'sent_time', 'is_read', 'read_time', 'related_id', 'created_at', 'updated_at']
        
        reminder_list = []
        for reminder in reminders:
            reminder_dict = dict(zip(columns, reminder))
            # 转换布尔值
            for key in ['is_sent', 'is_read']:
                if key in reminder_dict:
                    reminder_dict[key] = bool(reminder_dict[key])
            reminder_list.append(reminder_dict)
        
        return reminder_list
        
    except Exception as e:
        print(f"获取提醒历史失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取提醒历史失败: {str(e)}"
        )