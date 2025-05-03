from app.application.feature.queries.validate_walk_test_time_duration_query import ValidateWalkTestTimeDurationQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.read.read_walk_test_repository import ReadWalkTestRepository


class ValidateWalkTestTimeDurationQueryHandler(QueryHandler[ValidateWalkTestTimeDurationQuery,bool]):


    def __init__(self,read_walk_test_repository : ReadWalkTestRepository ,cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_walk_test_repository = read_walk_test_repository

    async def handle(self, query: ValidateWalkTestTimeDurationQuery) -> bool:
       is_valid = await self.read_walk_test_repository.validate_walk_test_execution_time(walk_test_id=query.walk_test_id)
       print(f"is_valid {is_valid}")
       return is_valid
