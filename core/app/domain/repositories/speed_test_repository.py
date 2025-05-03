from abc import  abstractmethod
from typing import List, Optional

from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain


class SpeedTestRepository:
    @abstractmethod
    async def save_all(self, results: List[SpeedTestServerDomain]) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[SpeedTestServerDomain]:
        pass

    @abstractmethod
    async def upsert_servers(self, servers: List[SpeedTestServerDomain]) -> None:
        pass
