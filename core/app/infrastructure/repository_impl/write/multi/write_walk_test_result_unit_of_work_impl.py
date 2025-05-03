from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.call_test_domain import CallTestDomain
from app.domain.entities.cell_info_domain import CellInfoDomain
from app.domain.entities.speed_test_result_domain import SpeedTestResultDomain
from app.domain.entities.walk_test_detail_domain import WalkTestDetailDomain

from app.domain.repositories.write.multi.write_walk_test_result_unit_of_work import WriteWalkTestResultUnitOfWork
from app.infrastructure.exceptions import DuplicateValueException
from app.infrastructure.mapper.mapper import  map_models_list
from app.infrastructure.repository_impl.write import BaseWriteDB
from app.infrastructure.schemas.table_call_test import TableCallTest
from app.infrastructure.schemas.table_cell_info import TableCellInfo
from app.infrastructure.schemas.table_speed_test_results import TableSpeedTestResults
from app.infrastructure.schemas.table_walk_test_detail import TableWalkTestDetail


class WriteWalkTestResultsUnitOfWorkImpl(BaseWriteDB, WriteWalkTestResultUnitOfWork):




    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)

    async def transact(self,walk_test_id : str, speed_test_result_domain: list[SpeedTestResultDomain],
                       cell_info_result_domain: list[CellInfoDomain], call_test_domain: list[CallTestDomain],
                       walk_test_detail_domain: list[WalkTestDetailDomain]) -> str:
        walk_test_detail_schema_model = await map_models_list(walk_test_detail_domain, TableWalkTestDetail)
        speed_test_schema_list = await map_models_list(speed_test_result_domain, TableSpeedTestResults)
        cell_info_schema_list = await map_models_list(cell_info_result_domain, TableCellInfo)
        call_test_schema_list = await map_models_list(call_test_domain, TableCallTest)
        async with self:
              result = await self.db.execute(
                select(TableWalkTestDetail).where(TableWalkTestDetail.walk_test_id == walk_test_id)
               )
              record = result.scalars().first()
              if record is None:
               self.db.add_all(walk_test_detail_schema_model)
               await self.db.flush()

               self.db.add_all(speed_test_schema_list)
               self.db.add_all(cell_info_schema_list)
               self.db.add_all(call_test_schema_list)
               return f"successfully inserted walk test result for walk test = {walk_test_id}"
              else:
                raise DuplicateValueException()


