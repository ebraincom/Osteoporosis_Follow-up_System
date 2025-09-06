#!/usr/bin/env python3
"""自动化备份脚本 - 在重要操作前自动创建备份"""

import os
import shutil
import json
import datetime
from pathlib import Path

def auto_backup(operation_name, files=None, db_backup=True):
    """自动创建备份"""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_id = f"auto_{operation_name}_{timestamp}"
    
    print(f"🔄 自动备份: {backup_id}")
    print(f"📝 操作: {operation_name}")
    
    # 创建备份目录
    backup_path = backup_dir / backup_id
    backup_path.mkdir(exist_ok=True)
    
    # 备份代码文件
    if files:
        code_backup_path = backup_path / "code"
        code_backup_path.mkdir(exist_ok=True)
        
        for file_path in files:
            if Path(file_path).exists():
                dest_path = code_backup_path / Path(file_path).name
                shutil.copy2(file_path, dest_path)
                print(f"  📄 备份文件: {file_path}")
    
    # 备份数据库
    if db_backup:
        db_backup_path = backup_path / "database"
        db_backup_path.mkdir(exist_ok=True)
        
        if Path("osteoporosis.db").exists():
            shutil.copy2("osteoporosis.db", db_backup_path / "osteoporosis.db")
            print(f"  🗄️  备份数据库: osteoporosis.db")
    
    # 记录备份信息
    backup_info = {
        "id": backup_id,
        "timestamp": timestamp,
        "operation": operation_name,
        "type": "auto",
        "files": files or [],
        "db_backup": db_backup,
        "backup_path": str(backup_path)
    }
    
    # 保存到自动备份记录
    auto_backup_file = backup_dir / "auto_backups.json"
    auto_backups = []
    
    if auto_backup_file.exists():
        with open(auto_backup_file, 'r', encoding='utf-8') as f:
            auto_backups = json.load(f)
    
    auto_backups.append(backup_info)
    
    with open(auto_backup_file, 'w', encoding='utf-8') as f:
        json.dump(auto_backups, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 自动备份完成: {backup_path}")
    return backup_id

def cleanup_old_backups(keep_count=5):
    """清理旧的自动备份，只保留最近的几个"""
    backup_dir = Path("backups")
    auto_backup_file = backup_dir / "auto_backups.json"
    
    if not auto_backup_file.exists():
        return
    
    with open(auto_backup_file, 'r', encoding='utf-8') as f:
        auto_backups = json.load(f)
    
    if len(auto_backups) <= keep_count:
        return
    
    # 按时间排序，保留最新的
    auto_backups.sort(key=lambda x: x['timestamp'], reverse=True)
    backups_to_keep = auto_backups[:keep_count]
    backups_to_delete = auto_backups[keep_count:]
    
    print(f"🧹 清理旧备份，保留最近 {keep_count} 个")
    
    for backup in backups_to_delete:
        backup_path = Path(backup['backup_path'])
        if backup_path.exists():
            shutil.rmtree(backup_path)
            print(f"  🗑️  删除: {backup['id']}")
    
    # 更新记录文件
    with open(auto_backup_file, 'w', encoding='utf-8') as f:
        json.dump(backups_to_keep, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 清理完成，保留 {len(backups_to_keep)} 个备份")

def list_auto_backups():
    """列出所有自动备份"""
    backup_dir = Path("backups")
    auto_backup_file = backup_dir / "auto_backups.json"
    
    if not auto_backup_file.exists():
        print("❌ 没有找到自动备份记录")
        return
    
    with open(auto_backup_file, 'r', encoding='utf-8') as f:
        auto_backups = json.load(f)
    
    print("📋 自动备份列表:")
    for backup in auto_backups:
        print(f"  {backup['id']} - {backup['timestamp']}")
        print(f"    操作: {backup['operation']}")
        print(f"    路径: {backup['backup_path']}")
        print()

def main():
    """主函数 - 用于测试"""
    print("🔄 骨质疏松症随访系统 - 自动备份工具")
    print("=" * 50)
    
    print("请选择操作:")
    print("1. 创建自动备份")
    print("2. 列出自动备份")
    print("3. 清理旧备份")
    print("4. 退出")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == "1":
        operation = input("请输入操作名称: ").strip()
        files_input = input("请输入要备份的文件路径 (用逗号分隔，回车跳过): ").strip()
        files = [f.strip() for f in files_input.split(",")] if files_input else None
        
        db_backup = input("是否备份数据库? (y/n, 默认y): ").strip().lower() != 'n'
        
        auto_backup(operation, files, db_backup)
    
    elif choice == "2":
        list_auto_backups()
    
    elif choice == "3":
        keep_count = input("请输入要保留的备份数量 (默认5): ").strip()
        keep_count = int(keep_count) if keep_count.isdigit() else 5
        cleanup_old_backups(keep_count)
    
    elif choice == "4":
        print("👋 再见！")
    
    else:
        print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main() 