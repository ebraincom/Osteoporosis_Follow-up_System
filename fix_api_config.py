#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API配置快速修复脚本
用于一键修复常见的API路径问题
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class APIConfigFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"
        self.backup_dir = self.project_root / "config_backups"
        
        # 确保备份目录存在
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self):
        """创建配置文件备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"config_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        print(f"📦 创建配置备份: {backup_name}")
        
        # 备份关键配置文件
        files_to_backup = [
            "frontend/src/utils/request.ts",
            "frontend/src/api/auth.ts",
            "frontend/src/api/patient.ts",
            "frontend/vite.config.ts",
            "backend-python/main.py"
        ]
        
        backup_path.mkdir(exist_ok=True)
        for file_path in files_to_backup:
            src_file = self.project_root / file_path
            if src_file.exists():
                dst_file = backup_path / file_path.split('/')[-1]
                shutil.copy2(src_file, dst_file)
                print(f"  ✅ 已备份: {file_path}")
        
        return backup_path
    
    def fix_request_ts(self):
        """修复request.ts中的baseURL配置"""
        print("🔧 修复 request.ts...")
        
        request_file = self.frontend_dir / "src" / "utils" / "request.ts"
        if not request_file.exists():
            print("  ❌ request.ts文件不存在")
            return False
        
        content = request_file.read_text(encoding='utf-8')
        
        # 修复baseURL
        content = re.sub(
            r'baseURL:\s*[\'"]([^\'"]*)[\'"]',
            'baseURL: \'/api\'',
            content
        )
        
        # 添加注释说明
        if '// ⚠️ 重要：不要修改这个值' not in content:
            content = content.replace(
                'baseURL: \'/api\',',
                'baseURL: \'/api\',  // ⚠️ 重要：不要修改这个值'
            )
        
        request_file.write_text(content, encoding='utf-8')
        print("  ✅ request.ts修复完成")
        return True
    
    def fix_auth_ts(self):
        """修复auth.ts中的API路径"""
        print("🔧 修复 auth.ts...")
        
        auth_file = self.frontend_dir / "src" / "api" / "auth.ts"
        if not auth_file.exists():
            print("  ❌ auth.ts文件不存在")
            return False
        
        content = auth_file.read_text(encoding='utf-8')
        
        # 修复所有API路径，移除重复的/api前缀
        content = re.sub(
            r'request\.(?:get|post|put|delete)\([\'"](/api/v1/[^\'"]*)[\'"]',
            lambda m: m.group(0).replace('/api/v1/', '/v1/'),
            content
        )
        
        auth_file.write_text(content, encoding='utf-8')
        print("  ✅ auth.ts修复完成")
        return True
    
    def fix_patient_ts(self):
        """修复patient.ts中的API路径"""
        print("🔧 修复 patient.ts...")
        
        patient_file = self.frontend_dir / "src" / "api" / "patient.ts"
        if not patient_file.exists():
            print("  ❌ patient.ts文件不存在")
            return False
        
        content = patient_file.read_text(encoding='utf-8')
        
        # 修复所有API路径，移除重复的/api前缀
        content = re.sub(
            r'request\.(?:get|post|put|delete)\([\'"](/api/v1/[^\'"]*)[\'"]',
            lambda m: m.group(0).replace('/api/v1/', '/v1/'),
            content
        )
        
        patient_file.write_text(content, encoding='utf-8')
        print("  ✅ patient.ts修复完成")
        return True
    
    def fix_vite_config(self):
        """修复vite.config.ts中的代理配置"""
        print("🔧 修复 vite.config.ts...")
        
        vite_file = self.frontend_dir / "vite.config.ts"
        if not vite_file.exists():
            print("  ❌ vite.config.ts文件不存在")
            return False
        
        content = vite_file.read_text(encoding='utf-8')
        
        # 确保代理配置正确
        if 'target: \'http://localhost:8000\'' not in content:
            # 如果代理配置不正确，使用标准配置替换
            proxy_config = '''
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
        },
        '/health': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
        },
      },
'''
            # 替换现有的代理配置
            content = re.sub(
                r'proxy:\s*{[^}]*}',
                proxy_config.strip(),
                content,
                flags=re.DOTALL
            )
        
        vite_file.write_text(content, encoding='utf-8')
        print("  ✅ vite.config.ts修复完成")
        return True
    
    def fix_all(self):
        """修复所有配置"""
        print("🚀 开始修复API配置...")
        
        # 创建备份
        backup_path = self.create_backup()
        print(f"📦 备份已保存到: {backup_path}")
        
        # 修复各个文件
        fixes = [
            self.fix_request_ts,
            self.fix_auth_ts,
            self.fix_patient_ts,
            self.fix_vite_config
        ]
        
        success_count = 0
        for fix_func in fixes:
            try:
                if fix_func():
                    success_count += 1
            except Exception as e:
                print(f"  ❌ 修复失败: {e}")
        
        print(f"\n📊 修复完成: {success_count}/{len(fixes)} 个文件修复成功")
        
        if success_count == len(fixes):
            print("🎉 所有配置修复完成！")
            print("💡 建议:")
            print("1. 重启前端服务")
            print("2. 测试登录功能")
            print("3. 检查患者列表加载")
        else:
            print("⚠️  部分配置修复失败，请检查错误信息")
        
        return success_count == len(fixes)
    
    def restore_backup(self, backup_name):
        """从备份恢复配置"""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            print(f"❌ 备份 {backup_name} 不存在")
            return False
        
        print(f"🔄 从备份恢复: {backup_name}")
        
        # 恢复文件
        files_to_restore = [
            "request.ts",
            "auth.ts", 
            "patient.ts",
            "vite.config.ts",
            "main.py"
        ]
        
        for file_name in files_to_restore:
            src_file = backup_path / file_name
            if src_file.exists():
                if file_name == "main.py":
                    dst_file = self.project_root / "backend-python" / file_name
                elif file_name == "vite.config.ts":
                    dst_file = self.frontend_dir / file_name
                elif file_name in ["request.ts"]:
                    dst_file = self.frontend_dir / "src" / "utils" / file_name
                else:
                    dst_file = self.frontend_dir / "src" / "api" / file_name
                
                shutil.copy2(src_file, dst_file)
                print(f"  ✅ 已恢复: {file_name}")
        
        print("🔄 配置恢复完成")
        return True
    
    def list_backups(self):
        """列出所有备份"""
        if not self.backup_dir.exists():
            print("📦 没有找到备份")
            return
        
        backups = list(self.backup_dir.glob("config_backup_*"))
        if not backups:
            print("📦 没有找到备份")
            return
        
        print("📦 可用的备份:")
        for backup in sorted(backups, reverse=True):
            backup_name = backup.name
            backup_time = backup.stat().st_mtime
            backup_date = datetime.fromtimestamp(backup_time).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {backup_name} - {backup_date}")

def main():
    import sys
    
    fixer = APIConfigFixer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "fix":
            fixer.fix_all()
        elif command == "restore":
            if len(sys.argv) > 2:
                backup_name = sys.argv[2]
                fixer.restore_backup(backup_name)
            else:
                print("用法: python fix_api_config.py restore <backup_name>")
        elif command == "list":
            fixer.list_backups()
        elif command == "check":
            # 运行配置检查
            os.system("python check_api_config.py")
        else:
            print("未知命令。可用命令:")
            print("  fix     - 修复所有配置")
            print("  restore - 从备份恢复")
            print("  list    - 列出所有备份")
            print("  check   - 检查配置状态")
    else:
        print("API配置修复工具")
        print("用法:")
        print("  python fix_api_config.py fix     - 修复所有配置")
        print("  python fix_api_config.py restore <backup_name> - 从备份恢复")
        print("  python fix_api_config.py list    - 列出所有备份")
        print("  python fix_api_config.py check   - 检查配置状态")

if __name__ == "__main__":
    main() 