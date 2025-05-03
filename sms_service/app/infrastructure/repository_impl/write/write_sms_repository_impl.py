from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sms_record_domain import SMSRecordDomain
from app.domain.repository.write.write_sms_repository import WriteSmsRepository
from app.infrastructure.mapper.mapper import map_models, map_models_list
from app.infrastructure.repository_impl.write import BaseWriteDB
from app.infrastructure.schemas.table_sms_record import TableSmsRecord


class WriteSmsRepositoryImpl(BaseWriteDB,WriteSmsRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)


    async def insert(self, sms_record_domain: SMSRecordDomain):
        async with self:
            print(f"result {sms_record_domain}",flush=True)
            result = await map_models(sms_record_domain, TableSmsRecord)
            print(f"result {result}",flush=True)
            self.db.add(result)



    async def insert_all(self, sms_record_domain_list: list[SMSRecordDomain]):
        async with self:
            result = await map_models_list(sms_record_domain_list, TableSmsRecord)
            self.db.add_all(result)