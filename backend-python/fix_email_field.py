import sqlite3

# 连接数据库
conn = sqlite3.connect('osteoporosis.db')
cursor = conn.cursor()

print("修复email字段约束...")

try:
    # 检查当前email字段约束
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for col in columns:
        if col[1] == 'email':
            print(f"当前email字段: {col}")
            break
    
    # 由于SQLite不支持直接修改列约束，我们需要重建表
    # 首先创建新表
    cursor.execute("""
        CREATE TABLE users_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE,
            hashed_password VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            user_type VARCHAR(13) NOT NULL,
            institution VARCHAR(200),
            department VARCHAR(100),
            age INTEGER,
            gender VARCHAR(6),
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0,
            avatar VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    """)
    
    # 复制数据
    cursor.execute("""
        INSERT INTO users_new 
        SELECT * FROM users
    """)
    
    # 删除旧表
    cursor.execute("DROP TABLE users")
    
    # 重命名新表
    cursor.execute("ALTER TABLE users_new RENAME TO users")
    
    # 创建索引
    cursor.execute("CREATE UNIQUE INDEX ix_users_username ON users (username)")
    cursor.execute("CREATE UNIQUE INDEX ix_users_email ON users (email)")
    
    conn.commit()
    print("✅ email字段约束修复成功")
    
    # 验证修复结果
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for col in columns:
        if col[1] == 'email':
            print(f"修复后email字段: {col}")
            break
            
except Exception as e:
    print(f"❌ 修复失败: {e}")
    conn.rollback()
finally:
    conn.close()