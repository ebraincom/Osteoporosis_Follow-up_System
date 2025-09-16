import sqlite3

def debug_followup_records():
    """调试随访记录"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 调试随访记录 ===")
    
    # 检查用户ID=4对应的患者记录
    print("\n=== 用户ID=4的患者记录 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = 4")
    patients = cursor.fetchall()
    
    for patient in patients:
        print(f"患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
        
        # 检查每个患者的随访记录
        cursor.execute("SELECT id, patient_id, time, method, details, patient_status FROM followup_records WHERE patient_id = ?", (patient[0],))
        followups = cursor.fetchall()
        
        print(f"  随访记录数量: {len(followups)}")
        for followup in followups:
            print(f"    - 随访ID: {followup[0]}, 患者ID: {followup[1]}, 时间: {followup[2]}, 方法: {followup[3]}, 状态: {followup[5]}")
    
    # 检查随访回复记录
    print("\n=== 随访回复记录 ===")
    cursor.execute("SELECT id, followup_id, patient_id, response_time, is_completed FROM followup_responses ORDER BY patient_id")
    responses = cursor.fetchall()
    
    for response in responses:
        print(f"回复ID: {response[0]}, 随访ID: {response[1]}, 患者ID: {response[2]}, 时间: {response[3]}, 完成: {response[4]}")

    conn.close()

if __name__ == "__main__":
    debug_followup_records()