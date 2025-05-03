from typing import Any, List

from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain
from app.domain.repositories.speed_test_repository import SpeedTestRepository
from app.infrastructure.services_impl.speed_test_crawler import SpeedTestServerCrawler


class SpeedTestServerListUseCase(BaseUseCase):

    def __init__(self, repository: SpeedTestRepository):
        self.repository = repository

    async def __execute__(self, **kwargs) -> List[SpeedTestServerDomain]:

        await self.repository.upsert_servers(servers=servers)

        return servers
        # Update the database
