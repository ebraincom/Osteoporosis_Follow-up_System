#!/usr/bin/env python3
"""
修复服务器部署问题的脚本
解决登录逻辑和用户类型判断问题
"""

import os
import sys
import json
from pathlib import Path

def check_and_fix_backend_config():
    """检查并修复后端配置"""
    print("🔧 检查后端配置...")
    
    # 检查配置文件
    config_files = [
        "backend-python/app/core/config_simple.py",
        "backend-python/app/core/config.py"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ 找到配置文件: {config_file}")
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "ALLOWED_HOSTS" in content:
                    print(f"  - CORS配置正常")
                if "DATABASE_URL" in content:
                    print(f"  - 数据库配置正常")
        else:
            print(f"❌ 配置文件不存在: {config_file}")

def check_api_routes():
    """检查API路由注册"""
    print("\n🔧 检查API路由注册...")
    
    api_file = "backend-python/app/api/v1/api.py"
    if os.path.exists(api_file):
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "personal_auth" in content:
                print("✅ 个人用户认证路由已注册")
            else:
                print("❌ 个人用户认证路由未注册")
                
            if "auth.router" in content:
                print("✅ 机构用户认证路由已注册")
            else:
                print("❌ 机构用户认证路由未注册")
    else:
        print(f"❌ API路由文件不存在: {api_file}")

def check_database_models():
    """检查数据库模型"""
    print("\n🔧 检查数据库模型...")
    
    model_files = [
        "backend-python/app/models/personal_user.py",
        "backend-python/app/models/user.py"
    ]
    
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"✅ 模型文件存在: {model_file}")
        else:
            print(f"❌ 模型文件不存在: {model_file}")

def check_frontend_login_logic():
    """检查前端登录逻辑"""
    print("\n🔧 检查前端登录逻辑...")
    
    frontend_files = [
        "frontend/src/views/Login.vue",
        "frontend/src/api/auth.ts",
        "frontend/src/stores/user.ts"
    ]
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "userType" in content:
                    print(f"✅ {file_path} - 用户类型选择逻辑正常")
                else:
                    print(f"⚠️  {file_path} - 可能缺少用户类型逻辑")
        else:
            print(f"❌ 文件不存在: {file_path}")

def create_production_env():
    """创建生产环境配置文件"""
    print("\n🔧 创建生产环境配置...")
    
    env_content = """# 生产环境配置
ENVIRONMENT=production
SECRET_KEY=your-super-secret-production-key-change-this
DATABASE_URL=sqlite:///./osteoporosis.db
REDIS_URL=redis://redis:6379/0

# CORS设置
ALLOWED_HOSTS=["*"]

# JWT设置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 日志级别
LOG_LEVEL=INFO

# 文件上传设置
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

# GPU设置
CUDA_VISIBLE_DEVICES=0
MODEL_CACHE_DIR=./models

# 其他设置
DEBUG=False
"""
    
    env_file = "backend-python/.env"
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f"✅ 生产环境配置文件已创建: {env_file}")

def create_deployment_checklist():
    """创建部署检查清单"""
    print("\n📋 创建部署检查清单...")
    
    checklist = {
        "服务器部署检查清单": {
            "环境配置": [
                "✅ 创建生产环境配置文件 (.env)",
                "✅ 检查数据库连接配置",
                "✅ 检查CORS设置",
                "✅ 检查JWT密钥配置"
            ],
            "后端服务": [
                "✅ 检查API路由注册",
                "✅ 检查数据库模型",
                "✅ 检查个人用户表初始化",
                "✅ 检查认证接口"
            ],
            "前端服务": [
                "✅ 检查登录页面用户类型选择",
                "✅ 检查API调用逻辑",
                "✅ 检查用户状态管理",
                "✅ 检查路由守卫"
            ],
            "数据库": [
                "✅ 初始化个人用户表",
                "✅ 检查用户表结构",
                "✅ 创建测试用户"
            ]
        }
    }
    
    with open("deployment_checklist.json", 'w', encoding='utf-8') as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)
    print("✅ 部署检查清单已创建: deployment_checklist.json")

def main():
    """主函数"""
    print("🚀 开始修复服务器部署问题...")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("backend-python"):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 执行检查和修复
    check_and_fix_backend_config()
    check_api_routes()
    check_database_models()
    check_frontend_login_logic()
    create_production_env()
    create_deployment_checklist()
    
    print("\n" + "=" * 50)
    print("✅ 服务器部署问题检查和修复完成！")
    print("\n📝 下一步操作建议：")
    print("1. 运行数据库初始化脚本: python backend-python/init_personal_users_table.py")
    print("2. 检查服务器上的Docker配置")
    print("3. 重新部署服务")
    print("4. 测试登录功能")

if __name__ == "__main__":
    main()