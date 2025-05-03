from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.complaint_type_domain import ComplaintTypeDomain
from app.domain.repositories.read.read_complaint_type_repository import ReadComplaintTypeRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_complaint_type import TableComplaintType


class ReadComplaintTypeRepositoryImpl(ReadComplaintTypeRepository):

    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_all(self) -> List[ComplaintTypeDomain]:
        result = await self.db.execute(
            select(TableComplaintType).order_by(TableComplaintType.id.asc())
        )
        records = result.scalars().all()
        complaint_type_list = await map_models_list(records, ComplaintTypeDomain)
        return complaint_type_list






