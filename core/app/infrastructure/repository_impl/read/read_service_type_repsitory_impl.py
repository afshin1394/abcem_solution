from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.service_type_domain import ServiceTypeDomain
from app.domain.repositories.read.read_service_type_repository import ReadServiceTypeRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_service_type import TableServiceType


class ReadServiceTypeRepositoryImpl(ReadServiceTypeRepository):


    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_all(self) -> List[ServiceTypeDomain]:
        result = await self.db.execute(
            select(TableServiceType).order_by(TableServiceType.id.asc())
        )
        records = result.scalars().all()
        service_type_list = await map_models_list(records, ServiceTypeDomain)
        return service_type_list