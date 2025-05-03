from typing import List

from app.application.feature.queries.get_all_problematic_service_type_query import GetAllProblematicServiceTypeQuery
from app.application.feature.shared.query_handler import QueryHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.problematic_service_domain import ProblematicServiceDomain
from app.domain.repositories.read.read_problematic_service_repository import ReadProblematicServiceRepository


class GetAllProblematicServiceTypeQueryHandler(QueryHandler[GetAllProblematicServiceTypeQuery,List[ProblematicServiceDomain]]):


    def __init__(self,read_problematic_service_type_repository : ReadProblematicServiceRepository ,cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 3600):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_problematic_service_type_repository = read_problematic_service_type_repository

    async def handle(self, query: GetAllProblematicServiceTypeQuery) -> List[ProblematicServiceDomain]:
        return await self.read_problematic_service_type_repository.get_all()
