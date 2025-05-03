from typing import Optional
from app.core.config import settings
from app.infrastructure.exceptions import RedisConnectionException, RedisGetException, RedisSetException
import aioredis
class RedisClient:
    _instance: Optional['RedisClient'] = None

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    @classmethod
    async def get_instance(cls, redis_url: str = settings.redis_url) -> 'RedisClient':
        try:
            if cls._instance is None:
                cls._instance = RedisClient(redis_url)
                cls._instance.redis = await aioredis.from_url(redis_url, decode_responses=True)
            return cls._instance
        except:
            raise RedisConnectionException()

    async def invalidate_keys(self, keys: list):
        if not keys:
            return
        await self.redis.delete(*keys)

    async def get(self, key: str):
        try:
            value = await self.redis.get(key)
            if value is None:
                raise RedisGetException(key=key)
        except:
            raise RedisGetException(key=key)

    async def set(self, key: str, value, expire: int = 3600):
        try:
            await self.redis.set(key, value, ex=expire)
            print(f'key : {key}')
        except:
            raise RedisSetException(key=key)
