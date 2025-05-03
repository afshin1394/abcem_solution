from typing import List

from app.application.feature.queries.get_all_complaint_type_query import GetAllComplaintTypeQuery
from app.application.feature.shared.query_handler import QueryHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.complaint_type_domain import ComplaintTypeDomain
from app.domain.repositories.read.read_complaint_type_repository import ReadComplaintTypeRepository


class GetAllComplaintTypeQueryHandler(QueryHandler[GetAllComplaintTypeQuery,List[ComplaintTypeDomain]]):
    def __init__(self, read_complaint_type_repository: ReadComplaintTypeRepository, cache_gateway: CacheGateway , expire : int):
        super().__init__(cache_gateway,expire=expire)
        self.read_complaint_type_repository = read_complaint_type_repository


    async def handle(self, query: GetAllComplaintTypeQuery) -> List[ComplaintTypeDomain]:
        result = await self.read_complaint_type_repository.get_all()
        return result