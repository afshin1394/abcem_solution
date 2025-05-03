from abc import ABC, abstractmethod

from app.domain.entities.walk_test_results_domain import WalkTestResultsDomain


class ReadWalkTestResultsRepository(ABC):
    @abstractmethod
    async def get_walk_test_results_by_id(self,walk_test_id : str) -> list[WalkTestResultsDomain]:
        raise NotImplementedError