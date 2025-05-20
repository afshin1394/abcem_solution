import uuid

from app.application.feature.commands.create_walk_test_results_command import CreateWalkTestResultsCommand
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.call_test_domain import CallTestDomain
from app.domain.entities.cell_info_domain import CellInfoDomain
from app.domain.entities.speed_test_result_domain import SpeedTestResultDomain
from app.domain.entities.walk_test_detail_domain import WalkTestDetailDomain
from app.interfaces.dto.request.walk_test_results_request import WalkTestResultsRequest


import uuid
from typing import List

class InsertWalkTestResultsUseCase(BaseUseCase):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    async def execute(self, **kwargs) -> str:
        walk_test_results_request = kwargs.get("walk_test_results_request")
        if isinstance(walk_test_results_request, WalkTestResultsRequest):
            print("walk_test_results_request: " + str(walk_test_results_request))
            create_walk_test_detail_command = await self.convert_walk_test_results_request_to_command(walk_test_results_request)
            return await self.mediator.send(create_walk_test_detail_command)
        else:
            print("The argument is not of type 'WalkTestResultsRequest'")



    @staticmethod
    async def convert_walk_test_results_request_to_command(walk_test_results_request : WalkTestResultsRequest) -> CreateWalkTestResultsCommand:
        walk_test_detail_list: List[WalkTestDetailDomain] = []
        speed_test_list: List[SpeedTestResultDomain] = []
        cell_info_list: List[CellInfoDomain] = []
        call_test_list: List[CallTestDomain] = []

        for step in walk_test_results_request.steps:
            walk_test_detail_id = str(uuid.uuid4())

            # Convert step metadata to WalkTestDetailDomain
            walk_test_detail_list.append(WalkTestDetailDomain(
                id=walk_test_detail_id,
                walk_test_id=walk_test_results_request.walk_test_id,
                step_number=step.step_number,
                step_type_id=step.step_type_id
            ))

            # Convert speed test results if available
            if step.speed_test_result:
                for speed in step.speed_test_result:
                    speed_test_list.append(SpeedTestResultDomain(
                        walk_test_detail_id=walk_test_detail_id,
                        download=speed.download,
                        upload=speed.upload,
                        ping=speed.ping,
                        jitter=speed.jitter
                    ))

            # Convert cell info results if available
            if step.cell_info_result:
                for cell in step.cell_info_result:
                    cell_info_list.append(CellInfoDomain(
                        walk_test_detail_id=walk_test_detail_id,
                        technology_id=cell.technology_id,
                        level=cell.level,
                        quality=cell.quality,
                        cell_data=cell.cell_data
                    ))

            # Convert call test results if available
            if step.call_test_result:
                for call in step.call_test_result:
                    call_test_list.append(CallTestDomain(
                        walk_test_detail_id=walk_test_detail_id,
                        drop_call=call.drop_call,
                        is_voltE=call.is_voltE,
                        technology_id=call.technology_id
                    ))

        # Create and return the final command
        return CreateWalkTestResultsCommand(
            walk_test_id=walk_test_results_request.walk_test_id,
            walk_test_detail_list=walk_test_detail_list,
            speed_test_list=speed_test_list,
            cell_info_list=cell_info_list,
            call_test_list=call_test_list
        )

