from app.application.feature.shared.command import Command
from app.domain.entities.call_test_domain import CallTestDomain
from app.domain.entities.cell_info_domain import CellInfoDomain
from app.domain.entities.speed_test_result_domain import SpeedTestResultDomain
from app.domain.entities.walk_test_detail_domain import WalkTestDetailDomain


class CreateWalkTestResultsCommand(Command):
    walk_test_id : str
    walk_test_detail_list : list[WalkTestDetailDomain]
    speed_test_list : list[SpeedTestResultDomain]
    cell_info_list : list[CellInfoDomain]
    call_test_list : list[CallTestDomain]
