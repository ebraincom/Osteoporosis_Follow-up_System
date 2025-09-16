import sqlite3
import uuid
from datetime import datetime

def create_patient_for_personal_users():
    """为个人用户创建对应的患者记录"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 检查需要创建患者记录的个人用户 ===")
    
    # 获取所有个人用户
    cursor.execute("""
        SELECT id, username, name, phone, age, gender, institution, 
               height, weight, t_score, z_score, risk_level, address,
               medical_history, family_history, medications
        FROM personal_users
    """)
    personal_users = cursor.fetchall()
    
    print(f"找到 {len(personal_users)} 个个人用户")
    
    for user in personal_users:
        user_id, username, name, phone, age, gender, institution, height, weight, t_score, z_score, risk_level, address, medical_history, family_history, medications = user
        
        # 检查是否已经有对应的患者记录
        cursor.execute("SELECT id FROM patients WHERE name = ?", (name,))
        existing_patient = cursor.fetchone()
        
        if existing_patient:
            print(f"✅ {name} 已有患者记录，ID: {existing_patient[0]}")
        else:
            # 生成患者编号
            patient_id = f"LH{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4().int)[:10]}"
            
            # 创建患者记录
            cursor.execute("""
                INSERT INTO patients (
                    patient_id, name, age, gender, phone, institution,
                    height, weight, t_score, z_score, risk_level, address,
                    medical_history, family_history, medications, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id, name, age, gender, phone, institution,
                height, weight, t_score, z_score, risk_level, address,
                medical_history, family_history, medications,
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
            
            new_patient_id = cursor.lastrowid
            print(f"✅ 为 {name} 创建患者记录，ID: {new_patient_id}, 患者编号: {patient_id}")

    conn.commit()
    conn.close()
    print("\n=== 完成 ===")

if __name__ == "__main__":
    create_patient_for_personal_users()