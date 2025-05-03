from abc import ABC, abstractmethod

from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain


class ReadSpeedTestServerRepository(ABC):

    @abstractmethod
    async def get_all(self) -> list[SpeedTestServerDomain]:
        raise NotImplementedError

