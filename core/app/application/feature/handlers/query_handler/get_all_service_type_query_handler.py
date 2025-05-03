from typing import List

from app.application.feature.queries.get_all_service_type_query import GetAllServiceTypeQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.service_type_domain import ServiceTypeDomain
from app.domain.repositories.read.read_service_type_repository import ReadServiceTypeRepository


class GetAllServiceTypeQueryHandler(QueryHandler[GetAllServiceTypeQuery,List[ServiceTypeDomain]]):

    def __init__(self,service_type_repository : ReadServiceTypeRepository , cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 3600):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.service_type_repository = service_type_repository

    async def handle(self, query: GetAllServiceTypeQuery) -> List[ServiceTypeDomain]:
       return await self.service_type_repository.get_all()
