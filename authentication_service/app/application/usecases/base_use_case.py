from abc import abstractmethod, ABC
from typing import Any

from app.application.exception import ApplicationException
from app.infrastructure.exceptions import InfrastructureException


class BaseUseCase(ABC):
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass

    async def run(self, **kwargs) -> Any:
        try:
            return await self.execute(**kwargs)
        except InfrastructureException as infra_exp:
            return infra_exp
        except ApplicationException as app_exp:
            return app_exp
        except Exception as e:
            return e



