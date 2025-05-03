from typing import List

from app.application.feature.queries.get_all_test_step_type_query import GetAllTestStepTypeQuery
from app.application.feature.shared.query_handler import QueryHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.step_test_type_domain import StepTestTypeDomain
from app.domain.repositories.read.read_test_step_type_repository import ReadTestStepTypeRepository


class GetAllTestStepTypeQueryHandler(QueryHandler[GetAllTestStepTypeQuery, List[StepTestTypeDomain]]):

    def __init__(self, read_step_test_type_repository: ReadTestStepTypeRepository, cache_gateway: CacheGateway,
                 cache_enabled: bool = True, expire: int = 3600):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_step_test_type_repository = read_step_test_type_repository

    async def handle(self, query: GetAllTestStepTypeQuery) -> List[StepTestTypeDomain]:
        return await self.read_step_test_type_repository.get_all()
