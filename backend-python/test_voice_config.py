#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config_simple import settings

def test_voice_config():
    """测试语音配置"""
    print("=== 语音交互配置测试 ===")
    
    print(f"豆包AI API Key: {'已配置' if settings.DOUBAO_API_KEY else '未配置'}")
    print(f"语音API Key: {'已配置' if settings.VOICE_API_KEY else '未配置'}")
    print(f"语音Endpoint ID: {'已配置' if settings.VOICE_ENDPOINT_ID else '未配置'}")
    print(f"语音模型: {settings.VOICE_MODEL}")
    print(f"采样率: {settings.VOICE_SAMPLE_RATE}")
    print(f"声道数: {settings.VOICE_CHANNELS}")
    
    # 检查环境变量
    print("\n=== 环境变量检查 ===")
    env_vars = [
        'DOUBAO_API_KEY',
        'VOICE_API_KEY', 
        'VOICE_ENDPOINT_ID'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"{var}: {'已设置' if value else '未设置'}")
        else:
            print(f"{var}: 未设置")
    
    print("\n=== 配置建议 ===")
    if not settings.DOUBAO_API_KEY and not settings.VOICE_API_KEY:
        print("❌ 需要配置API Key")
        print("请在.env文件中添加:")
        print("DOUBAO_API_KEY=your_api_key_here")
        print("或者")
        print("VOICE_API_KEY=your_voice_api_key_here")
    
    if not settings.VOICE_ENDPOINT_ID:
        print("⚠️  建议配置VOICE_ENDPOINT_ID用于实时语音交互")
        print("VOICE_ENDPOINT_ID=your_endpoint_id_here")
    
    if settings.DOUBAO_API_KEY or settings.VOICE_API_KEY:
        print("✅ API Key配置正常")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_voice_config()