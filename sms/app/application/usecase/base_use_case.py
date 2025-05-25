from abc import ABC, abstractmethod
from typing import Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseUseCase(ABC):
    """
    Abstract base class for use cases.
    Provides a pipeline for executing use cases with logging and exception handling.
    """

    async def __call__(self, *args, **kwargs) -> Any:
        try:
            logger.info(f"Starting use case: {self.__class__.__name__}")
            print(f"Starting use case: {self.__class__.__name__}", flush=True)

            result = await self.execute(**kwargs)

            logger.info(f"Use case {self.__class__.__name__} completed successfully")
            print(f"Use case {self.__class__.__name__} completed successfully", flush=True)
            return result

        except Exception as e:
            logger.error(f"Error in use case {self.__class__.__name__}: {str(e)}", exc_info=True)
            print(f"Use case {self.__class__.__name__} failed with error: {e}", flush=True)
            raise

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass
