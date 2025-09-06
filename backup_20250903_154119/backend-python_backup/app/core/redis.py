import redis.asyncio as redis
from app.core.config import settings

# 创建Redis客户端
redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

# Redis连接测试
async def test_redis_connection():
    try:
        await redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return False 