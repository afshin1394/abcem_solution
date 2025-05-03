from app.application.feature.queries.get_walk_test_coordinates_query import GetWalkTestCoordinatesQuery
from app.application.feature.shared.query_handler import QueryHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.read.read_walk_test_repository import ReadWalkTestRepository



class GetWalkTestCoordinatesQueryHandler(QueryHandler[GetWalkTestCoordinatesQuery, tuple[float, float]]):


    def __init__(self,read_walk_test_repository : ReadWalkTestRepository, cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_walk_test_repository = read_walk_test_repository

    async def handle(self, query: GetWalkTestCoordinatesQuery) -> tuple[float, float]:
       return await self.read_walk_test_repository.get_coordinates(walk_test_id=query.walk_test_id)