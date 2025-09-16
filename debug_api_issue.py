import sys
import os

# 切换到backend-python目录
os.chdir('backend-python')
sys.path.append('.')

from app.core.database import SessionLocal
from app.crud import patient as patient_crud

def debug_api_issue():
    """调试API问题"""
    db = SessionLocal()
    
    try:
        print("=== 调试API问题 ===")
        
        # 测试获取用户ID=1的患者列表
        print("测试获取用户ID=1的患者列表...")
        patients = patient_crud.get_patients(db, user_id=1, limit=10)
        print(f"找到 {len(patients)} 个患者")
        
        for patient in patients:
            print(f"  - 患者ID: {patient.id}, 姓名: {patient.name}, 用户ID: {patient.user_id}")
        
        # 测试获取用户ID=4的患者列表
        print("\n测试获取用户ID=4的患者列表...")
        patients = patient_crud.get_patients(db, user_id=4, limit=10)
        print(f"找到 {len(patients)} 个患者")
        
        for patient in patients:
            print(f"  - 患者ID: {patient.id}, 姓名: {patient.name}, 用户ID: {patient.user_id}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_api_issue()