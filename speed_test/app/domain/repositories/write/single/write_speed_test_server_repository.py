from abc import ABC, abstractmethod

from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain


class WriteSpeedTestServerRepository(ABC):



    @abstractmethod
    async def update_all(self, servers : list[SpeedTestServerDomain]):
        raise NotImplementedError()