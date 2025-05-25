from app.application.feature.queries.get_n_last_sms_query import GetNLastSmsRecordsQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities import PaginatedResult
from app.domain.entities.sms_record_domain import SMSRecordDomain
from app.domain.repository.read.read_sms_repository import ReadSmsRepository


class GetNLastSMSRecordQueryHandler(QueryHandler[GetNLastSmsRecordsQuery,PaginatedResult[SMSRecordDomain]]):


    def __init__(self,read_sms_repository : ReadSmsRepository, cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_sms_repository = read_sms_repository

    async def handle(self, query: GetNLastSmsRecordsQuery) -> PaginatedResult[SMSRecordDomain]:
        result  = await self.read_sms_repository.get_n_last_sms(page=query.page, page_size=query.page_size)
        print(f"result: {result}",flush=True)
        return result
