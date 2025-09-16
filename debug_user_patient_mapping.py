import sqlite3

def debug_user_patient_mapping():
    """调试用户和患者的映射关系"""
    db_path = 'backend-python/osteoporosis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=== 调试用户和患者映射关系 ===")
    
    # 检查个人用户表
    print("\n=== 个人用户表 ===")
    cursor.execute("SELECT id, username, name FROM personal_users ORDER BY id")
    personal_users = cursor.fetchall()
    
    for user in personal_users:
        print(f"ID: {user[0]}, 用户名: {user[1]}, 姓名: {user[2]}")
    
    # 检查患者表
    print("\n=== 患者表 ===")
    cursor.execute("SELECT id, name, user_id FROM patients ORDER BY user_id, id")
    patients = cursor.fetchall()
    
    for patient in patients:
        print(f"患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
    
    # 检查赵一御的具体信息
    print("\n=== 赵一御的信息 ===")
    cursor.execute("SELECT id, username, name FROM personal_users WHERE username = '赵一御'")
    zhao_user = cursor.fetchone()
    
    if zhao_user:
        print(f"赵一御 - ID: {zhao_user[0]}, 用户名: {zhao_user[1]}, 姓名: {zhao_user[2]}")
        
        # 检查赵一御对应的患者记录
        cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = ?", (zhao_user[0],))
        zhao_patients = cursor.fetchall()
        
        print(f"赵一御对应的患者记录数量: {len(zhao_patients)}")
        for patient in zhao_patients:
            print(f"  - 患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")
    else:
        print("❌ 没有找到赵一御用户")
    
    # 检查李一御的信息
    print("\n=== 李一御的信息 ===")
    cursor.execute("SELECT id, username, name FROM personal_users WHERE name = '李一御'")
    li_users = cursor.fetchall()
    
    for li_user in li_users:
        print(f"李一御 - ID: {li_user[0]}, 用户名: {li_user[1]}, 姓名: {li_user[2]}")
        
        # 检查李一御对应的患者记录
        cursor.execute("SELECT id, name, user_id FROM patients WHERE user_id = ?", (li_user[0],))
        li_patients = cursor.fetchall()
        
        print(f"李一御对应的患者记录数量: {len(li_patients)}")
        for patient in li_patients:
            print(f"  - 患者ID: {patient[0]}, 姓名: {patient[1]}, 用户ID: {patient[2]}")

    conn.close()

if __name__ == "__main__":
    debug_user_patient_mapping()