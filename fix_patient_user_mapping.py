import sqlite3

def fix_patient_user_mapping():
    """修复患者和用户的映射关系"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 修复患者和用户映射关系 ===")
    
    # 检查当前的问题
    print("\n=== 当前问题 ===")
    cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = 4")
    patients = cursor.fetchall()
    
    for patient in patients:
        print(f"患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
    
    # 修复方案：将患者ID=10（李一御）的user_id改为正确的用户ID
    # 首先找到真正的李一御用户ID
    cursor.execute("SELECT id FROM personal_users WHERE username = '李一御' AND name = '李一御'")
    real_li_user = cursor.fetchone()
    
    if real_li_user:
        real_li_user_id = real_li_user[0]
        print(f"\n真正的李一御用户ID: {real_li_user_id}")
        
        # 将患者ID=10（李一御）的user_id改为真正的李一御用户ID
        cursor.execute("UPDATE patients SET user_id = ? WHERE id = 10", (real_li_user_id,))
        updated_count = cursor.rowcount
        print(f"更新了 {updated_count} 条患者记录")
        
        # 验证修复结果
        print("\n=== 修复后的结果 ===")
        cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = 4")
        zhao_patients = cursor.fetchall()
        print(f"赵一御（用户ID=4）的患者记录:")
        for patient in zhao_patients:
            print(f"  患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
        
        cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = ?", (real_li_user_id,))
        li_patients = cursor.fetchall()
        print(f"李一御（用户ID={real_li_user_id}）的患者记录:")
        for patient in li_patients:
            print(f"  患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
    else:
        print("❌ 没有找到真正的李一御用户")
    
    conn.commit()
    conn.close()
    print("\n✅ 患者用户映射关系修复完成")

if __name__ == "__main__":
    fix_patient_user_mapping()