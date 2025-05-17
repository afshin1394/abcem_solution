from app.domain.cache.cache_gateway import CacheGateway
from app.infrastructure.redis import RedisCacheGateway


async def get_cache() -> CacheGateway:
    return await RedisCacheGateway.get_instance()
