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
    async def get_instance(cls, redis_url: str = f'{settings.redis_url}'):
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

    async def list_push(self, key: str, value: Any):
        """
        Pushes the `value` to the left of the Redis list stored at `key`.
        The value is serialized before being pushed to the list.

        :param key: The key of the Redis list.
        :param value: The value to push to the list.
        """
        # Serialize the value to store it in Redis (if it's not already a string)
        serialized_value = json.dumps(value)

        # Push to the left side of the list (FIFO queue-like behavior)
        await self.redis.lpush(key, serialized_value)
    async def list_blocking_pop(self, key: str, timeout: int = 0) -> Optional[Any]:
        """
        Pops the last element from the Redis list stored at `key`, blocking up to `timeout` seconds
        if the list is empty. This supports FIFO queue behavior when paired with LPUSH.

        :param key: The key of the Redis list.
        :param timeout: How long to block in seconds (0 means block indefinitely).
        :return: The deserialized value popped from the list, or None if timed out.
        """
        result = await self.redis.brpop(key, timeout=timeout)
        if result:
            _, value = result  # result is a (key, value) tuple
            return json.loads(value)
        return None