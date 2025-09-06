#!/usr/bin/env python3
"""快速回滚脚本 - 紧急情况下的快速回滚"""

import os
import shutil
import sqlite3
from pathlib import Path

def quick_rollback():
    """快速回滚到最近的稳定版本"""
    print("🚨 快速回滚模式")
    print("=" * 50)
    
    # 检查是否有备份
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("❌ 没有找到备份目录")
        return False
    
    # 查找最新的备份
    backups = [d for d in backup_dir.iterdir() if d.is_dir() and d.name.startswith('v')]
    if not backups:
        print("❌ 没有找到可用的备份")
        return False
    
    # 按版本号排序，找到最新的
    latest_backup = sorted(backups, key=lambda x: x.name)[-1]
    print(f"📦 找到最新备份: {latest_backup.name}")
    
    # 确认回滚
    confirm = input(f"确认回滚到 {latest_backup.name}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 回滚已取消")
        return False
    
    print(f"🔄 开始快速回滚...")
    
    # 回滚数据库
    db_backup = latest_backup / "database" / "osteoporosis.db"
    if db_backup.exists():
        print("🗄️  回滚数据库...")
        try:
            shutil.copy2(db_backup, "osteoporosis.db")
            print("  ✅ 数据库回滚成功")
        except Exception as e:
            print(f"  ❌ 数据库回滚失败: {e}")
            return False
    
    # 回滚代码文件
    code_backup = latest_backup / "code"
    if code_backup.exists():
        print("📄 回滚代码文件...")
        for backup_file in code_backup.iterdir():
            if backup_file.is_file():
                try:
                    # 尝试找到对应的源文件
                    source_file = Path(backup_file.name)
                    if source_file.exists():
                        shutil.copy2(backup_file, source_file)
                        print(f"  ✅ 回滚: {source_file}")
                except Exception as e:
                    print(f"  ⚠️  回滚失败: {backup_file.name} - {e}")
    
    print(f"✅ 快速回滚完成: {latest_backup.name}")
    print("💡 建议重启服务以确保回滚生效")
    return True

def emergency_rollback():
    """紧急回滚 - 强制回滚到指定备份"""
    print("🚨 紧急回滚模式")
    print("=" * 50)
    
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("❌ 没有找到备份目录")
        return False
    
    # 列出所有备份
    backups = [d for d in backup_dir.iterdir() if d.is_dir() and d.name.startswith('v')]
    if not backups:
        print("❌ 没有找到可用的备份")
        return False
    
    print("📋 可用备份:")
    for i, backup in enumerate(backups):
        print(f"  {i+1}. {backup.name}")
    
    try:
        choice = int(input("\n请选择要回滚的备份 (输入序号): ")) - 1
        if 0 <= choice < len(backups):
            selected_backup = backups[choice]
        else:
            print("❌ 无效选择")
            return False
    except ValueError:
        print("❌ 请输入有效数字")
        return False
    
    print(f"🔄 开始紧急回滚到: {selected_backup.name}")
    
    # 强制回滚数据库
    db_backup = selected_backup / "database" / "osteoporosis.db"
    if db_backup.exists():
        print("🗄️  强制回滚数据库...")
        try:
            # 先备份当前数据库
            if Path("osteoporosis.db").exists():
                shutil.copy2("osteoporosis.db", "osteoporosis.db.emergency_backup")
                print("  📦 当前数据库已备份为 osteoporosis.db.emergency_backup")
            
            shutil.copy2(db_backup, "osteoporosis.db")
            print("  ✅ 数据库回滚成功")
        except Exception as e:
            print(f"  ❌ 数据库回滚失败: {e}")
            return False
    
    # 强制回滚代码文件
    code_backup = selected_backup / "code"
    if code_backup.exists():
        print("📄 强制回滚代码文件...")
        for backup_file in code_backup.iterdir():
            if backup_file.is_file():
                try:
                    source_file = Path(backup_file.name)
                    shutil.copy2(backup_file, source_file)
                    print(f"  ✅ 回滚: {source_file}")
                except Exception as e:
                    print(f"  ⚠️  回滚失败: {backup_file.name} - {e}")
    
    print(f"✅ 紧急回滚完成: {selected_backup.name}")
    print("🚨 请立即重启服务！")
    return True

def main():
    """主函数"""
    print("🚨 骨质疏松症随访系统 - 快速回滚工具")
    print("=" * 50)
    
    print("请选择回滚模式:")
    print("1. 快速回滚 (推荐)")
    print("2. 紧急回滚 (强制)")
    print("3. 退出")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        quick_rollback()
    elif choice == "2":
        emergency_rollback()
    elif choice == "3":
        print("👋 再见！")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 