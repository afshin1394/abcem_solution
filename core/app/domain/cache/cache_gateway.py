from abc import ABC, abstractmethod
from typing import Optional, List, Any


class CacheGateway(ABC):
    @abstractmethod
    async def set(self, key: str, value: Any, expire: int) -> None:
        """
        Stores a value of type T under the specified key, with an expiry time.
        """
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value of type T for the specified key, if present.
        """
        pass

    @abstractmethod
    async def invalidate_keys(self, keys: List[str]) -> None:
        """
        Deletes the specified keys from the cache, invalidating them.
        """
        pass
    @abstractmethod
    async def sadd(self, key: str,value : Any,expire: int = 2592000):
        """
        Set in set data structure
        """
        raise NotImplementedError()

    @abstractmethod
    async def sys_member(self,key:str,value: Any):
        """
            Lookup the set
        """
        raise NotImplementedError()

