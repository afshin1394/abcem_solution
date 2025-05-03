from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.problematic_service_domain import ProblematicServiceDomain
from app.domain.repositories.read.read_problematic_service_repository import ReadProblematicServiceRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_problematic_service import TableProblematicService


class ReadProblematicServiceRepositoryImpl(ReadProblematicServiceRepository):

    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_all(self) -> List[ProblematicServiceDomain]:
        result = await self.db.execute(
            select(TableProblematicService).order_by(TableProblematicService.id.asc())
        )
        records = result.scalars().all()
        problematic_service_list = await map_models_list(records, ProblematicServiceDomain)
        return problematic_service_list
