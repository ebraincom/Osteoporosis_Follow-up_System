#!/usr/bin/env python3
"""版本控制脚本 - 管理代码和数据库的版本"""

import os
import shutil
import sqlite3
import json
import datetime
from pathlib import Path

class VersionControl:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.version_file = self.backup_dir / "versions.json"
        self.load_versions()
    
    def load_versions(self):
        """加载版本信息"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                self.versions = json.load(f)
        else:
            self.versions = []
    
    def save_versions(self):
        """保存版本信息"""
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, ensure_ascii=False, indent=2)
    
    def create_backup(self, description, files=None, db_backup=True):
        """创建备份"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        version_id = f"v{len(self.versions) + 1}_{timestamp}"
        
        print(f"🔄 创建备份: {version_id}")
        print(f"📝 描述: {description}")
        
        # 创建备份目录
        backup_path = self.backup_dir / version_id
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
        
        # 记录版本信息
        version_info = {
            "id": version_id,
            "timestamp": timestamp,
            "description": description,
            "files": files or [],
            "db_backup": db_backup,
            "backup_path": str(backup_path)
        }
        
        self.versions.append(version_info)
        self.save_versions()
        
        print(f"✅ 备份完成: {backup_path}")
        return version_id
    
    def list_versions(self):
        """列出所有版本"""
        print("📋 版本列表:")
        for version in self.versions:
            print(f"  {version['id']} - {version['timestamp']}")
            print(f"    描述: {version['description']}")
            print(f"    路径: {version['backup_path']}")
            print()
    
    def rollback_to_version(self, version_id):
        """回滚到指定版本"""
        version = None
        for v in self.versions:
            if v['id'] == version_id:
                version = v
                break
        
        if not version:
            print(f"❌ 版本 {version_id} 不存在")
            return False
        
        print(f"🔄 开始回滚到版本: {version_id}")
        print(f"📝 描述: {version['description']}")
        
        backup_path = Path(version['backup_path'])
        
        # 回滚代码文件
        if version['files']:
            code_backup_path = backup_path / "code"
            if code_backup_path.exists():
                print("📄 回滚代码文件...")
                for file_path in version['files']:
                    if Path(file_path).exists():
                        backup_file = code_backup_path / Path(file_path).name
                        if backup_file.exists():
                            shutil.copy2(backup_file, file_path)
                            print(f"  ✅ 回滚: {file_path}")
        
        # 回滚数据库
        if version['db_backup']:
            db_backup_path = backup_path / "database"
            if db_backup_path.exists():
                print("🗄️  回滚数据库...")
                db_backup_file = db_backup_path / "osteoporosis.db"
                if db_backup_file.exists():
                    shutil.copy2(db_backup_file, "osteoporosis.db")
                    print(f"  ✅ 回滚数据库: osteoporosis.db")
        
        print(f"✅ 回滚完成: {version_id}")
        return True
    
    def delete_version(self, version_id):
        """删除指定版本"""
        version = None
        for i, v in enumerate(self.versions):
            if v['id'] == version_id:
                version = v
                del self.versions[i]
                break
        
        if not version:
            print(f"❌ 版本 {version_id} 不存在")
            return False
        
        # 删除备份文件
        backup_path = Path(version['backup_path'])
        if backup_path.exists():
            shutil.rmtree(backup_path)
            print(f"🗑️  删除备份目录: {backup_path}")
        
        self.save_versions()
        print(f"✅ 版本 {version_id} 已删除")
        return True

def main():
    """主函数"""
    vc = VersionControl()
    
    print("🔄 骨质疏松症随访系统 - 版本控制工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建备份")
        print("2. 列出版本")
        print("3. 回滚到指定版本")
        print("4. 删除版本")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == "1":
            description = input("请输入备份描述: ").strip()
            files_input = input("请输入要备份的文件路径 (用逗号分隔，回车跳过): ").strip()
            files = [f.strip() for f in files_input.split(",")] if files_input else None
            
            db_backup = input("是否备份数据库? (y/n, 默认y): ").strip().lower() != 'n'
            
            vc.create_backup(description, files, db_backup)
        
        elif choice == "2":
            vc.list_versions()
        
        elif choice == "3":
            vc.list_versions()
            version_id = input("请输入要回滚的版本ID: ").strip()
            if version_id:
                vc.rollback_to_version(version_id)
        
        elif choice == "4":
            vc.list_versions()
            version_id = input("请输入要删除的版本ID: ").strip()
            if version_id:
                confirm = input(f"确认删除版本 {version_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    vc.delete_version(version_id)
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main() 