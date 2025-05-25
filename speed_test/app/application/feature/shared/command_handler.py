# ir/irancell/application/shared/command_handler.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.events.event import Event


# Define a base Command class if not already defined
class Command:
    pass


# Define Type Variables with bounds
C = TypeVar('C', bound=Command)
E = TypeVar('E', bound=Event)


class CommandHandler(ABC, Generic[C, E]):
    """
    Abstract base class for handling commands and producing events.

    Args:
        C: A type variable bound to a Command subclass.
        E: A type variable bound to an Event subclass or None.
    """

    def __init__(self, cache_gateway: CacheGateway):
        self.cache_gateway = cache_gateway

    @abstractmethod
    async def handle(self, command: C) -> Optional[E]:
        """
        Handle the given command and optionally produce an event.

        Args:
            command (C): The command to handle.

        Returns:
            Optional[E]: The resulting event or None.
        """
        pass

    async def __call__(self, command: C) -> Optional[E]:
        """Executes the command and invalidates cache if needed"""
        result = await self.handle(command)

        # Determine affected cache keys dynamically
        cache_keys_to_invalidate = await self.get_related_cache_keys(command)
        print(f"cache_keys_to_invalidate{cache_keys_to_invalidate}")
        if cache_keys_to_invalidate:
            await self.cache_gateway.invalidate_keys(cache_keys_to_invalidate)
        return result


    @abstractmethod
    async def get_related_cache_keys(self, command: C) -> list[str]:
        """
        Override this method in subclasses to return a list of cache keys to invalidate
        based on the executed command.
        """
        return []

