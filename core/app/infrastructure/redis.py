# infrastructure/cache/redis_client.py
import json
from typing import Optional,Any

from redis.asyncio import Redis

from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway


class RedisCacheGateway(CacheGateway):
    _instance: Optional['RedisCacheGateway'] = None

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    @classmethod
    async def get_instance(cls, redis_url: str = f'{settings.redis_url}') -> 'CacheGateway':
        if cls._instance is None:
            cls._instance = RedisCacheGateway(redis_url)
            cls._instance.redis = await Redis.from_url(redis_url, decode_responses=True)
        return cls._instance

    async def invalidate_keys(self, keys: list):
        print(f"redis keys:{keys}")
        if not keys:
            return
        await self.redis.delete(*keys)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value is None:
            return None
        # Example of JSON-deserialization
        return json.loads(value)

    async def set(self, key: str, value: Any, expire: int = 3600):
            serialized = json.dumps(value)
            if expire > 0:
                await self.redis.set(key, serialized, ex=expire)
            else:
                await self.redis.set(key, serialized)
