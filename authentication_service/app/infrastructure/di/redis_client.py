from app.infrastructure.redis import RedisClient


async def get_redis_instance() -> RedisClient:
     return await RedisClient.get_instance()
