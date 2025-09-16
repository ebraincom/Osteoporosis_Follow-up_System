import sqlite3
import uuid
from datetime import datetime

def sync_personal_users_to_patients():
    """为所有个人用户创建对应的患者记录"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 同步个人用户到患者表 ===")
    
    # 获取所有个人用户
    cursor.execute("""
        SELECT id, username, name, phone, age, gender, institution, 
               height, weight, t_score, z_score, risk_level, address,
               medical_history, family_history, medications, created_at
        FROM personal_users
    """)
    personal_users = cursor.fetchall()
    
    print(f"找到 {len(personal_users)} 个个人用户")
    
    synced_count = 0
    for user in personal_users:
        user_id, username, name, phone, age, gender, institution, height, weight, t_score, z_score, risk_level, address, medical_history, family_history, medications, created_at = user
        
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
                    patient_id, name, age, gender, phone, email, address,
                    height, weight, t_score, z_score, risk_level,
                    medical_history, family_history, medications, user_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id, name, age, gender, phone, '', address,
                height, weight, t_score, z_score, risk_level,
                medical_history, family_history, medications, user_id, created_at
            ))
            
            new_patient_id = cursor.lastrowid
            synced_count += 1
            print(f"✅ 为 {name} 创建患者记录，ID: {new_patient_id}, 患者编号: {patient_id}")

    conn.commit()
    conn.close()
    print(f"\n=== 完成，共同步了 {synced_count} 个用户 ===")

if __name__ == "__main__":
    sync_personal_users_to_patients()