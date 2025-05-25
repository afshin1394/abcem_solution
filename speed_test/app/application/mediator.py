import inspect
from typing import Type, Callable, Dict, Any
import logging


class Mediator:
    def __init__(self):
        self._handlers: Dict[Type, Callable[[Any], Any]] = {}

    def register_handler(self, message_type: Type, handler: Callable[[Any], Any]):
        self._handlers[message_type] = handler

    async def send(self, message: Any = None) -> Any:
        logging.debug("\nsend\n")
        message_type = type(message)
        handler = self._handlers.get(message_type)
        if not handler:
            raise ValueError(f"No handler registered for {message_type}")

        # Call the handler first, then check if the result is awaitable.
        result = handler(message)
        if inspect.isawaitable(result):
            return await result
        return result
