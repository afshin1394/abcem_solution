from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.walk_test_domain import WalkTestDomain


class ReadWalkTestRepository(ABC):
    @abstractmethod
    async def get_all_by_msisdn(self, msisdn: str) -> List[WalkTestDomain]:
        raise NotImplementedError

    @abstractmethod
    async def validate_walk_test_execution_time(self,walk_test_id : str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def has_entered_at_value(self,walk_test_id : str) :
        raise NotImplementedError

    @abstractmethod
    async def get_coordinates(self,walk_test_id : str) -> tuple[float, float] :
        raise NotImplementedError
