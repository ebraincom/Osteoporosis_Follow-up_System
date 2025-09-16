import sqlite3

def recheck_and_fix():
    """重新检查并修复数据"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 重新检查并修复数据 ===")
    
    # 检查患者ID=13的记录
    print("\n=== 检查患者ID=13的记录 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE id = 13")
    patient_13 = cursor.fetchone()
    
    if patient_13:
        print(f"患者ID: {patient_13[0]}, 姓名: {patient_13[1]}, 用户ID: {patient_13[2]}")
        
        if patient_13[2] != 4:  # 如果user_id不是4
            print("❌ 患者ID=13的user_id不正确，应该是4")
            cursor.execute("UPDATE patients SET user_id = 4 WHERE id = 13")
            print("✅ 已修复患者ID=13的user_id为4")
        else:
            print("✅ 患者ID=13的user_id正确")
    
    # 检查患者ID=10的记录
    print("\n=== 检查患者ID=10的记录 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE id = 10")
    patient_10 = cursor.fetchone()
    
    if patient_10:
        print(f"患者ID: {patient_10[0]}, 姓名: {patient_10[1]}, 用户ID: {patient_10[2]}")
        
        if patient_10[2] != 1:  # 如果user_id不是1
            print("❌ 患者ID=10的user_id不正确，应该是1")
            cursor.execute("UPDATE patients SET user_id = 1 WHERE id = 10")
            print("✅ 已修复患者ID=10的user_id为1")
        else:
            print("✅ 患者ID=10的user_id正确")
    
    # 验证修复结果
    print("\n=== 验证修复结果 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE id IN (10, 13) ORDER BY id")
    patients = cursor.fetchall()
    
    for patient in patients:
        print(f"患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
    
    conn.commit()
    conn.close()
    print("\n✅ 数据修复完成")

if __name__ == "__main__":
    recheck_and_fix()