from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import PaginatedResult
from app.domain.entities.sms_record_domain import SMSRecordDomain
from app.domain.repository.read.read_sms_repository import ReadSmsRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.repository_impl.read import BaseReadRepositoryImpl
from app.infrastructure.schemas.table_sms_record import TableSmsRecord


class ReadSmsRepositoryImpl(BaseReadRepositoryImpl, ReadSmsRepository):


    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_n_last_sms(self,page : int ,page_size : int) -> PaginatedResult[SMSRecordDomain]:
        query = select(TableSmsRecord).order_by(
            TableSmsRecord.updated_at.asc()
        )

        # Apply pagination manually here (simple way)
        query = self.apply_pagination(query, page, page_size)
        paginated_result = await self.paginate_query(
            base_query=query,
            model=TableSmsRecord,
            page=page,
            page_size=page_size,
            map_func=lambda records: map_models_list(records, SMSRecordDomain)
        )
        print(f"paginated_result {paginated_result}",flush=True)

        return paginated_result


