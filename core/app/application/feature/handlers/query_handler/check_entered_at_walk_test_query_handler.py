from app.application.feature.queries.check_entered_at_walk_test_query import CheckEnteredAtWalkTestQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.read.read_walk_test_repository import ReadWalkTestRepository


class CheckEnteredAtWalkTestQueryHandler(QueryHandler[CheckEnteredAtWalkTestQuery, bool]):

    def __init__(self, read_walk_test_repository: ReadWalkTestRepository, cache_gateway: CacheGateway,
                 cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_walk_test_repository = read_walk_test_repository

    async def handle(self, query: CheckEnteredAtWalkTestQuery) -> bool:
        return await self.read_walk_test_repository.has_entered_at_value(walk_test_id=query.walk_test_id)
