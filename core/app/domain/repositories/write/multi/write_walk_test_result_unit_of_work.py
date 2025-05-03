from abc import ABC, abstractmethod

from app.domain.entities.call_test_domain import CallTestDomain
from app.domain.entities.cell_info_domain import CellInfoDomain
from app.domain.entities.speed_test_result_domain import SpeedTestResultDomain
from app.domain.entities.walk_test_detail_domain import WalkTestDetailDomain


class WriteWalkTestResultUnitOfWork(ABC):
    @abstractmethod
    async def transact(self,walk_test_id : str, speed_test_result_domain: list[SpeedTestResultDomain],
                       cell_info_result_domain: list[CellInfoDomain], call_test_domain: list[CallTestDomain],walk_test_detail_domain : list[WalkTestDetailDomain]):
          raise NotImplementedError()
