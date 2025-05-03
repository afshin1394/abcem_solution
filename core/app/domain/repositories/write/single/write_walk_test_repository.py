from abc import ABC, abstractmethod

from app.domain.entities.walk_test_domain import WalkTestDomain
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum


class WriteWalkTestRepository(ABC):
    @abstractmethod
    async def create_walk_test(self,walk_test_domain : WalkTestDomain) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_walk_test_status(self,walk_test_id : str,walk_test_status : WalkTestStatusEnum) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_entered_at(self, walk_test_id: str):
        raise NotImplementedError()

