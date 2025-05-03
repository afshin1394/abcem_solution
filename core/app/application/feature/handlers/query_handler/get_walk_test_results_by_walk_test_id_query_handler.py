from typing import List

from app.application.feature.queries.get_walk_test_results_by_walk_test_id_query import GetWalkTestResultsByWalkTestIdQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.walk_test_results_domain import WalkTestResultsDomain
from app.domain.repositories.read.read_walk_test_results_repository import ReadWalkTestResultsRepository


class GetWalkTestResultsByWalkTestIdQueryHandler(QueryHandler[GetWalkTestResultsByWalkTestIdQuery,List[WalkTestResultsDomain]]):

    def __init__(self,read_walk_test_results_repository: ReadWalkTestResultsRepository, cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway,expire=expire,cache_enabled=cache_enabled)
        self.read_walk_test_results_repository = read_walk_test_results_repository


    async def handle(self, query: GetWalkTestResultsByWalkTestIdQuery) -> list[WalkTestResultsDomain]:
        walk_test_results = await self.read_walk_test_results_repository.get_walk_test_results_by_id(walk_test_id=query.walk_test_id)
        print("walk_test_results"+walk_test_results.__str__())
        return  walk_test_results