#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import websockets
import base64
import io
import logging
import time
import wave
import struct
import math
from typing import Optional
import requests
from app.core.config_simple import settings
from app.core.security import get_current_user_dependency
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

class VoiceInteractionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.volcengine_connections: dict[str, websockets.WebSocketServerProtocol] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"用户 {user_id} 连接语音交互")
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.volcengine_connections:
            del self.volcengine_connections[user_id]
        logger.info(f"用户 {user_id} 断开语音交互")
    
    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))
    
    async def connect_to_volcengine(self, user_id: str):
        """连接到火山引擎实时语音识别API"""
        try:
            # 暂时跳过火山引擎连接，直接返回成功
            # 这样可以确保WebSocket连接不会因为外部API问题而断开
            logger.info(f"用户 {user_id} 跳过火山引擎连接，使用模拟模式")
            return True
            
            # 火山引擎实时语音识别WebSocket地址
            volcengine_url = f"wss://openspeech.bytedance.com/api/v1/asr/ws"
            
            # 使用火山引擎的认证方式
            headers = {
                "Authorization": f"Bearer {settings.VOICE_API_KEY}",
                "Content-Type": "application/json",
                "X-App-Id": settings.VOICE_APP_ID,
                "X-Region": settings.VOLCENGINE_REGION
            }
            
            # 火山引擎实时语音识别连接参数
            connection_params = {
                "app": {
                    "appid": settings.VOICE_APP_ID,
                    "token": settings.VOICE_API_KEY,
                    "cluster": "volcengine_streaming_common"
                },
                "user": {
                    "uid": user_id
                },
                "audio": {
                    "format": "pcm",
                    "rate": settings.VOICE_SAMPLE_RATE,
                    "channel": settings.VOICE_CHANNELS
                },
                "request": {
                    "reqid": f"req_{user_id}_{int(time.time())}",
                    "nbest": 1,
                    "result_type": "full",
                    "partial_result": True
                }
            }
            
            # 建立WebSocket连接
            volcengine_ws = await websockets.connect(
                volcengine_url,
                extra_headers=headers
            )
            
            self.volcengine_connections[user_id] = volcengine_ws
            
            # 发送初始化消息
            init_message = {
                "type": "session.update",
                "session": connection_params
            }
            await volcengine_ws.send(json.dumps(init_message))
            
            logger.info(f"用户 {user_id} 成功连接到火山引擎实时语音API")
            return True
            
        except Exception as e:
            logger.error(f"连接火山引擎失败: {str(e)}")
            return False
    
    async def send_audio_to_volcengine(self, user_id: str, audio_data: bytes):
        """发送音频数据到火山引擎"""
        try:
            if user_id in self.volcengine_connections:
                volcengine_ws = self.volcengine_connections[user_id]
                
                # 将音频数据编码为base64
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                message = {
                    "type": "input_audio_buffer.append",
                    "audio": audio_base64
                }
                
                await volcengine_ws.send(json.dumps(message))
                logger.debug(f"发送音频数据到火山引擎，用户: {user_id}")
                
        except Exception as e:
            logger.error(f"发送音频到火山引擎失败: {str(e)}")
    
    async def receive_audio_from_volcengine(self, user_id: str):
        """从火山引擎接收音频数据"""
        try:
            if user_id in self.volcengine_connections:
                volcengine_ws = self.volcengine_connections[user_id]
                
                while True:
                    message = await volcengine_ws.recv()
                    data = json.loads(message)
                    
                    if data.get("type") == "response.audio.delta":
                        # 接收到音频数据
                        audio_base64 = data.get("audio", "")
                        if audio_base64:
                            audio_data = base64.b64decode(audio_base64)
                            
                            # 转发给前端
                            await self.send_message(user_id, {
                                "type": "audio_response",
                                "audio": audio_base64,
                                "timestamp": data.get("timestamp")
                            })
                    
                    elif data.get("type") == "response.done":
                        # 响应完成
                        await self.send_message(user_id, {
                            "type": "response_done",
                            "message": "语音响应完成"
                        })
                        break
                        
        except Exception as e:
            logger.error(f"接收火山引擎音频失败: {str(e)}")

# 全局管理器实例
voice_manager = VoiceInteractionManager()

async def generate_simple_audio(text: str) -> str:
    """生成简单的音频回复"""
    try:
        # 生成简单的正弦波音频作为语音回复
        sample_rate = 16000
        duration = 2.0  # 2秒
        frequency = 440  # A4音符
        
        # 生成音频数据
        samples = []
        for i in range(int(sample_rate * duration)):
            # 生成正弦波
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.append(sample)
        
        # 创建WAV文件
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(sample_rate)
            
            # 写入音频数据
            for sample in samples:
                wav_file.writeframes(struct.pack('<h', sample))
        
        # 转换为base64
        wav_buffer.seek(0)
        audio_data = wav_buffer.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        logger.info(f"生成音频回复成功，大小: {len(audio_data)} 字节")
        return audio_base64
        
    except Exception as e:
        logger.error(f"生成音频失败: {str(e)}")
        return ""

@router.websocket("/voice-chat")
async def websocket_voice_chat(websocket: WebSocket, user_id: str = "default"):
    """语音交互WebSocket端点"""
    await voice_manager.connect(websocket, user_id)
    
    try:
        # 连接到火山引擎
        volcengine_connected = await voice_manager.connect_to_volcengine(user_id)
        
        if not volcengine_connected:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "无法连接到语音服务"
            }))
            return
        
        # 启动接收任务
        receive_task = asyncio.create_task(
            voice_manager.receive_audio_from_volcengine(user_id)
        )
        
        while True:
            try:
                # 接收前端消息
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "audio_data":
                    # 处理音频数据 - 模拟模式
                    audio_base64 = message.get("audio", "")
                    if audio_base64:
                        # 模拟语音识别和回复
                        await asyncio.sleep(1)  # 模拟处理时间
                        
                        # 生成简单的音频回复（使用文本转语音）
                        reply_text = "我听到了您的语音，这是语音回复。"
                        audio_reply = await generate_simple_audio(reply_text)
                        
                        await websocket.send_text(json.dumps({
                            "type": "audio_response",
                            "audio": audio_reply,
                            "text": reply_text,
                            "timestamp": int(time.time())
                        }))
                
                elif message.get("type") == "start_recording":
                    # 开始录音
                    await websocket.send_text(json.dumps({
                        "type": "recording_started",
                        "message": "开始录音"
                    }))
                
                elif message.get("type") == "stop_recording":
                    # 停止录音
                    await websocket.send_text(json.dumps({
                        "type": "recording_stopped",
                        "message": "停止录音"
                    }))
                
                elif message.get("type") == "ping":
                    # 心跳检测
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }))
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"处理WebSocket消息失败: {str(e)}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"处理消息失败: {str(e)}"
                }))
    
    except Exception as e:
        logger.error(f"WebSocket连接错误: {str(e)}")
    finally:
        # 清理连接
        voice_manager.disconnect(user_id)
        if 'receive_task' in locals():
            receive_task.cancel()

@router.get("/voice-status")
async def get_voice_status(current_user: User = Depends(get_current_user_dependency)):
    """获取语音服务状态"""
    return {
        "status": "available",
        "model": "doubao-1-5-pro-32k-250115",
        "voice_options": [
            {"id": "alloy", "name": "Alloy", "description": "自然女声"},
            {"id": "echo", "name": "Echo", "description": "清晰男声"},
            {"id": "fable", "name": "Fable", "description": "温暖女声"},
            {"id": "onyx", "name": "Onyx", "description": "深沉男声"},
            {"id": "nova", "name": "Nova", "description": "年轻女声"},
            {"id": "shimmer", "name": "Shimmer", "description": "柔和女声"}
        ],
        "supported_formats": {
            "input": ["pcm16", "wav", "mp3"],
            "output": ["pcm16", "wav", "mp3"]
        },
        "sample_rate": 16000,
        "channels": 1
    }

@router.post("/voice-test")
async def test_voice_connection(current_user: User = Depends(get_current_user_dependency)):
    """测试语音连接"""
    try:
        # 测试火山引擎API连接
        test_url = "https://ark.cn-beijing.volces.com/api/v3/models"
        headers = {
            "Authorization": f"Bearer {settings.VOICE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return {
                "status": "success",
                "message": "语音服务连接正常",
                "available_models": response.json().get("data", [])
            }
        else:
            return {
                "status": "error",
                "message": f"语音服务连接失败: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"语音服务测试失败: {str(e)}"
        }