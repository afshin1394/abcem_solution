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
        """
               Executes the use case pipeline.
               Handles logging and exceptions automatically.
               """
        try:
            # Log the start of the use case
            logger.info(f"Starting use case: {self.__class__.__name__}")
            print(f"Starting use case: {self.__class__.__name__}")

            # Execute the use case logic
            result = await self.__execute__(**kwargs)

            # Log the successful completion of the use case
            logger.info(f"Use case {self.__class__.__name__} completed successfully")
            print(f"Use case {self.__class__.__name__} completed successfully")
            return result

        except Exception as e:
            # Log the exception
            logger.error(f"Error in use case {self.__class__.__name__}: {str(e)}", exc_info=True)
            raise  # Re-raise the exception for further handling



    @abstractmethod
    async def __execute__(self, **kwargs) -> Any:
        """
        Abstract method to be implemented by child classes.
        Contains the core logic of the use case.
        """
        pass
