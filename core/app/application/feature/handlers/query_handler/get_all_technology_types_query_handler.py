from typing import List

from app.application.feature.queries.get_all_technology_types_query import GetAllTechnologyTypesQuery
from app.application.feature.shared.query_handler import QueryHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.technology_type_domain import TechnologyTypeDomain
from app.domain.repositories.read.read_technology_repository import ReadTechnologyRepository


class GetAllTechnologyTypesQueryHandler(QueryHandler[GetAllTechnologyTypesQuery, TechnologyTypeDomain]):

    def __init__(self, read_technology_repository: ReadTechnologyRepository, cache_gateway: CacheGateway,expire : int) -> None:
        super().__init__(cache_gateway,expire = expire)
        self.read_technology_repository = read_technology_repository

    async def handle(self, query: GetAllTechnologyTypesQuery) -> List[TechnologyTypeDomain]:
        return await self.read_technology_repository.get_all()


