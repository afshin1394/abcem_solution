from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.service_type_domain import ServiceTypeDomain


class ReadServiceTypeRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[ServiceTypeDomain]:
        pass
