
from app.application.feature.queries.get_all_speed_test_servers_query import GetAllSpeedTestServersQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain
from app.domain.repositories.read.read_speed_test_server_repository import ReadSpeedTestServerRepository


class GetAllSpeedTestServersQueryHandler(QueryHandler[GetAllSpeedTestServersQuery, list[SpeedTestServerDomain]]):




    def __init__(self, read_speed_test_server_repository : ReadSpeedTestServerRepository,cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_speed_test_server_repository = read_speed_test_server_repository

    async def handle(self, query: GetAllSpeedTestServersQuery) -> list[SpeedTestServerDomain]:
        servers = await self.read_speed_test_server_repository.get_all()
        return servers
