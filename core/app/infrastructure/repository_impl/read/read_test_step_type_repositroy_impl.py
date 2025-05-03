from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.step_test_type_domain import StepTestTypeDomain
from app.domain.repositories.read.read_test_step_type_repository import ReadTestStepTypeRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_step_type import TableStepTestType


class ReadTestStepTypeRepositoryImpl(ReadTestStepTypeRepository):


    def __init__(self, db : AsyncSession):
        self.db = db

    async def get_all(self) -> List[StepTestTypeDomain]:
        result = await self.db.execute(
            select(TableStepTestType).order_by(TableStepTestType.id.asc())
        )
        records = result.scalars().all()
        step_test_type_list = await map_models_list(records, StepTestTypeDomain)
        return step_test_type_list
