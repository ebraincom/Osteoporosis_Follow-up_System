from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import dashscope
from dashscope import Generation
import google.generativeai as genai
import json
import logging
from datetime import datetime
import requests

from app.core.config_simple import settings
from app.core.security import get_current_user_dependency
from app.models.user import User

router = APIRouter()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 请求模型
class AIQuestionRequest(BaseModel):
    question: str
    style: str = "concise"  # concise, detailed, professional
    model: str = "qwen"  # qwen, gemini, doubao
    user_id: Optional[int] = None

class AIAnswerResponse(BaseModel):
    answer: str
    model: str
    style: str
    timestamp: str

# 初始化通义千问
def init_qwen():
    """初始化通义千问API"""
    if not settings.QWEN_API_KEY:
        raise HTTPException(status_code=500, detail="通义千问API密钥未配置")
    
    dashscope.api_key = settings.QWEN_API_KEY
    logger.info("通义千问API初始化成功")

# 获取AI回答
def get_qwen_answer(question: str, style: str = "concise") -> str:
    """调用通义千问获取回答"""
    try:
        # 根据风格构建不同的提示词
        style_prompts = {
            "concise": "请简洁明了地回答以下问题，控制在100字以内：",
            "detailed": "请详细回答以下问题，提供全面的信息和解释：",
            "professional": "请以专业医生的角度回答以下问题，使用医学术语："
        }
        
        prompt = style_prompts.get(style, style_prompts["concise"])
        full_question = f"{prompt}\n\n问题：{question}"
        
        # 调用通义千问API
        response = Generation.call(
            model=settings.QWEN_MODEL,
            prompt=full_question,
            max_tokens=settings.QWEN_MAX_TOKENS,
            temperature=settings.QWEN_TEMPERATURE
        )
        
        if response.status_code == 200:
            return response.output.text
        else:
            logger.error(f"通义千问API调用失败: {response.message}")
            return "抱歉，AI服务暂时不可用，请稍后再试。"
            
    except Exception as e:
        logger.error(f"调用通义千问API时发生错误: {str(e)}")
        return "抱歉，AI服务暂时不可用，请稍后再试。"

# 初始化Google Gemini
def init_gemini():
    """初始化Google Gemini API"""
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Google Gemini API密钥未配置")
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    logger.info("Google Gemini API初始化成功")

# 获取Gemini回答
def get_gemini_answer(question: str, style: str = "concise") -> str:
    """调用Google Gemini获取回答"""
    try:
        # 根据风格构建不同的提示词
        style_prompts = {
            "concise": "Please provide a concise answer to the following question in Chinese, keep it under 100 words:",
            "detailed": "Please provide a detailed answer to the following question in Chinese, with comprehensive information and explanations:",
            "professional": "Please answer the following question from a professional medical perspective in Chinese, using medical terminology:"
        }
        
        prompt = style_prompts.get(style, style_prompts["concise"])
        full_question = f"{prompt}\n\n问题：{question}"
        
        # 调用Gemini API
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content(full_question)
        
        if response.text:
            return response.text
        else:
            logger.error("Gemini API返回空响应")
            return "抱歉，AI服务暂时不可用，请稍后再试。"
            
    except Exception as e:
        logger.error(f"调用Google Gemini API时发生错误: {str(e)}")
        return "抱歉，AI服务暂时不可用，请稍后再试。"

# 初始化豆包AI
def init_doubao():
    """初始化豆包AI API"""
    if not settings.DOUBAO_API_KEY:
        raise HTTPException(status_code=500, detail="豆包AI API密钥未配置")
    
    logger.info("豆包AI API初始化成功")

# 获取豆包AI回答
def get_doubao_answer(question: str, style: str = "concise") -> str:
    """调用豆包AI获取回答"""
    try:
        # 根据风格构建不同的提示词
        style_prompts = {
            "concise": "请简洁明了地回答以下问题，控制在100字以内：",
            "detailed": "请详细回答以下问题，提供全面的信息和解释：",
            "professional": "请以专业医生的角度回答以下问题，使用医学术语："
        }
        
        system_prompt = style_prompts.get(style, style_prompts["concise"])
        
        # 构建豆包AI API请求
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.DOUBAO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "doubao-1-5-pro-32k-250115",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": settings.DOUBAO_MAX_TOKENS,
            "temperature": settings.DOUBAO_TEMPERATURE
        }
        
        # 调用豆包AI API
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                logger.error("豆包AI API返回格式错误")
                return "抱歉，AI服务暂时不可用，请稍后再试。"
        else:
            logger.error(f"豆包AI API调用失败: {response.status_code} - {response.text}")
            return "抱歉，AI服务暂时不可用，请稍后再试。"
            
    except Exception as e:
        logger.error(f"调用豆包AI API时发生错误: {str(e)}")
        return "抱歉，AI服务暂时不可用，请稍后再试。"

@router.post("/ask", response_model=AIAnswerResponse)
async def ask_ai_question(
    request: AIQuestionRequest,
    current_user: User = Depends(get_current_user_dependency)
):
    """AI问答接口"""
    try:
        answer = ""
        model_name = ""
        
        # 根据选择的模型调用相应的AI
        if request.model == "qwen":
            # 初始化通义千问
            init_qwen()
            answer = get_qwen_answer(request.question, request.style)
            model_name = "qwen-turbo"
            
        elif request.model == "gemini":
            # 初始化Google Gemini
            init_gemini()
            answer = get_gemini_answer(request.question, request.style)
            model_name = "gemini-pro"
            
            
        elif request.model == "doubao":
            # 初始化豆包AI
            init_doubao()
            answer = get_doubao_answer(request.question, request.style)
            model_name = "doubao-pro-4k"
            
        else:
            raise HTTPException(status_code=400, detail=f"不支持的AI模型: {request.model}")
        
        # 返回响应
        return AIAnswerResponse(
            answer=answer,
            model=model_name,
            style=request.style,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"AI问答接口错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI问答服务错误: {str(e)}")

@router.get("/health")
async def ai_health_check():
    """AI服务健康检查"""
    try:
        models_status = {}
        
        # 检查通义千问配置
        if settings.QWEN_API_KEY:
            try:
                init_qwen()
                models_status["qwen"] = "available"
            except Exception as e:
                models_status["qwen"] = f"error: {str(e)}"
        else:
            models_status["qwen"] = "not_configured"
        
        # 检查Google Gemini配置
        if settings.GEMINI_API_KEY:
            try:
                init_gemini()
                models_status["gemini"] = "available"
            except Exception as e:
                models_status["gemini"] = f"error: {str(e)}"
        else:
            models_status["gemini"] = "not_configured"
        
        
        # 检查豆包AI配置
        if settings.DOUBAO_API_KEY:
            try:
                init_doubao()
                models_status["doubao"] = "available"
            except Exception as e:
                models_status["doubao"] = f"error: {str(e)}"
        else:
            models_status["doubao"] = "not_configured"
        
        # 检查是否有可用的模型
        available_models = [k for k, v in models_status.items() if v == "available"]
        
        if available_models:
            return {
                "status": "success",
                "message": f"AI服务正常，可用模型: {', '.join(available_models)}",
                "models": models_status
            }
        else:
            return {
                "status": "warning",
                "message": "没有可用的AI模型",
                "models": models_status
            }
        
    except Exception as e:
        return {"status": "error", "message": f"AI服务异常: {str(e)}"}

@router.get("/models")
async def get_available_models():
    """获取可用的AI模型列表"""
    models = []
    
    # 通义千问
    if settings.QWEN_API_KEY:
        models.append({
            "id": "qwen",
            "name": "通义千问",
            "description": "阿里云通义千问大模型",
            "available": True
        })
    
    # Google Gemini
    if settings.GEMINI_API_KEY:
        models.append({
            "id": "gemini",
            "name": "Google Gemini",
            "description": "Google Gemini大模型",
            "available": True
        })
    
    
    # 豆包AI
    if settings.DOUBAO_API_KEY:
        models.append({
            "id": "doubao",
            "name": "豆包AI",
            "description": "字节跳动豆包AI大模型",
            "available": True
        })
    
    return {"models": models}