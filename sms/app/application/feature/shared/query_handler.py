from abc import ABC, abstractmethod
from typing import Generic, TypeVar
import orjson


from app.domain.cache.cache_gateway import CacheGateway
from .query import Query  # import your Query base class

Q = TypeVar('Q', bound=Query)  # The specific Query type
R = TypeVar('R')  # The result type (whatever your query returns)


class QueryHandler(ABC, Generic[Q, R]):
    """
    Abstract base class for handling queries and producing results.
    """

    def __init__(self, cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        self.identifier = None
        self.cache_gateway = cache_gateway
        self.cache_enabled = cache_enabled  # Flag to enable/disable caching
        self.expire = expire

    @abstractmethod
    async def handle(self, query: Q) -> R:
        """
              Handle the given query and return the result.

              Args:
                  query (Q): The query to handle.

              Returns:
                  R: The result of the query.
              """
        pass


    async def __call__(self, query: Q) -> dict:
        """Process the query and utilize caching where applicable."""
        cache_key = await query.generate_cache_key()

        if self.cache_enabled:
            cached_result = await self.cache_gateway.get(cache_key)
            if cached_result:
                return orjson.loads(cached_result)

        # Execute query
        result = await self.handle(query)

        # Store in cache
        if self.cache_enabled:
            await self.cache_gateway.set(cache_key, orjson.dumps(result).decode(), expire=self.expire)

        return result
