#!/usr/bin/env python3
"""
初始化个人用户表的脚本
"""

import sqlite3
import os

def init_personal_users_table():
    """初始化个人用户表"""
    db_path = "osteoporosis.db"
    
    if not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建个人用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT,
                age INTEGER,
                gender TEXT,
                institution TEXT,
                is_active INTEGER DEFAULT 1,
                is_verified INTEGER DEFAULT 0,
                avatar TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_personal_users_username ON personal_users(username)")
        
        conn.commit()
        print("✅ 个人用户表创建成功")
        
        # 检查表结构
        cursor.execute("PRAGMA table_info(personal_users)")
        columns = cursor.fetchall()
        print("\n📋 个人用户表结构:")
        for col in columns:
            nullable = "NULL" if col[3] == 1 else "NOT NULL"
            print(f"  {col[1]} ({col[2]}) - {nullable} - default: {col[4]}")
        
        # 测试插入空值
        print("\n🧪 测试插入空值...")
        try:
            cursor.execute("""
                INSERT INTO personal_users (username, hashed_password, name, phone, age, gender, institution)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("test_user", "hashed_pass", "Test User", None, None, None, None))
            
            # 回滚测试数据
            conn.rollback()
            print("✅ 空值插入测试成功 - 字段确实是可选的")
        except Exception as e:
            print(f"❌ 空值插入测试失败: {e}")
            
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 开始初始化个人用户表...")
    init_personal_users_table()
    print("✨ 初始化完成!") 