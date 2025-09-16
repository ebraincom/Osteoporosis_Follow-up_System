import sqlite3

def verify_data_fix():
    """验证数据修复结果"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 验证数据修复结果 ===")
    
    # 检查赵一御（用户ID=4）的患者记录
    print("\n=== 赵一御（用户ID=4）的患者记录 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = 4")
    zhao_patients = cursor.fetchall()
    
    print(f"患者记录数量: {len(zhao_patients)}")
    for patient in zhao_patients:
        print(f"  患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
        
        # 检查每个患者的随访记录
        cursor.execute("SELECT COUNT(*) FROM followup_records WHERE patient_id = ?", (patient[0],))
        followup_count = cursor.fetchone()[0]
        print(f"    随访记录数量: {followup_count}")
    
    # 检查李一御（用户ID=1）的患者记录
    print("\n=== 李一御（用户ID=1）的患者记录 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = 1")
    li_patients = cursor.fetchall()
    
    print(f"患者记录数量: {len(li_patients)}")
    for patient in li_patients:
        print(f"  患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
        
        # 检查每个患者的随访记录
        cursor.execute("SELECT COUNT(*) FROM followup_records WHERE patient_id = ?", (patient[0],))
        followup_count = cursor.fetchone()[0]
        print(f"    随访记录数量: {followup_count}")
        
        # 检查待回复的随访记录
        cursor.execute("""
            SELECT COUNT(*) FROM followup_records fr
            LEFT JOIN followup_responses fresp ON fr.id = fresp.followup_id
            WHERE fr.patient_id = ? AND fresp.id IS NULL
        """, (patient[0],))
        pending_count = cursor.fetchone()[0]
        print(f"    待回复记录数量: {pending_count}")

    conn.close()
    print("\n✅ 数据验证完成")

if __name__ == "__main__":
    verify_data_fix()