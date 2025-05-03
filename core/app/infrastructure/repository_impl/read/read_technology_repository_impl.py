from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.technology_type_domain import TechnologyTypeDomain
from app.domain.repositories.read.read_technology_repository import ReadTechnologyRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_technology_type import TableTechnologyType


class ReadTechnologyRepositoryImpl(ReadTechnologyRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> List[TechnologyTypeDomain]:
        result = await self.db.execute(
            select(TableTechnologyType).order_by(TableTechnologyType.id.asc())
        )
        records = result.scalars().all()
        technology_list = await map_models_list(records, TechnologyTypeDomain)
        return technology_list
