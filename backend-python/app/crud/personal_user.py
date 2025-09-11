from sqlalchemy.orm import Session
from app.models.personal_user import PersonalUser
from app.schemas.personal_user import PersonalUserCreate
from app.core.security import get_password_hash

def get_personal_user_by_username(db: Session, username: str):
    """根据用户名获取个人用户"""
    return db.query(PersonalUser).filter(PersonalUser.username == username).first()

def get_personal_user_by_id(db: Session, user_id: int):
    """根据ID获取个人用户"""
    return db.query(PersonalUser).filter(PersonalUser.id == user_id).first()

def create_personal_user(db: Session, user: PersonalUserCreate):
    """创建个人用户"""
    try:
        hashed_password = get_password_hash(user.password)
        db_user = PersonalUser(
            username=user.username,
            hashed_password=hashed_password,
            name=user.name,
            phone=user.phone,
            age=user.age,
            gender=user.gender,
            institution=user.institution
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"创建个人用户数据库错误: {str(e)}")
        raise e

def update_personal_user(db: Session, user_id: int, user_update):
    """更新个人用户信息"""
    db_user = get_personal_user_by_id(db, user_id)
    if not db_user:
        return None
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_personal_user(db: Session, user_id: int):
    """删除个人用户"""
    db_user = get_personal_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def get_all_personal_users(db: Session, skip: int = 0, limit: int = 100):
    """获取所有个人用户"""
    return db.query(PersonalUser).offset(skip).limit(limit).all() 