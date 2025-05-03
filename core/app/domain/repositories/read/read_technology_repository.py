from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.technology_type_domain import TechnologyTypeDomain


class ReadTechnologyRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[TechnologyTypeDomain]:
        pass
