from app.application.usecase.get_walk_test_results_by_walk_test_id_use_case import GetWalkTestResultsByWalkTestIdUseCase
from app.application.usecase.insert_walk_test_results_use_case import InsertWalkTestResultsUseCase
from app.interfaces.dto.request.walk_test_results_by_walk_test_id_request import WalkTestResultsByWalkTestIdRequest
from app.interfaces.dto.request.walk_test_results_request import WalkTestResultsRequest
from app.interfaces.dto.response.walk_test_results_by_walk_test_id_response import WalkTestResultsByWalkTestIdResponse
from app.interfaces.dto.response.walk_test_results_response import WalkTestResultsResponse


class WalkTestResultsController:

    def __init__(self,
             insert_walk_test_results_use_case: InsertWalkTestResultsUseCase,
             get_walk_test_results_by_walk_test_id_use_case: GetWalkTestResultsByWalkTestIdUseCase,
             ):
         self.insert_walk_test_results_use_case = insert_walk_test_results_use_case
         self.get_walk_test_results_by_walk_test_id_use_case = get_walk_test_results_by_walk_test_id_use_case



    async def receive_walk_test_results(self,walk_test_results_request : WalkTestResultsRequest) -> WalkTestResultsResponse:
        result = await self.insert_walk_test_results_use_case(walk_test_results_request=walk_test_results_request)
        return WalkTestResultsResponse(status_code = 201,result = result)

    async def get_walk_test_results_by_walk_test_id(self,walk_test_results_by_walk_test_id_request : WalkTestResultsByWalkTestIdRequest) -> WalkTestResultsByWalkTestIdResponse:
        walk_test_results_with_device_info_composition = await self.get_walk_test_results_by_walk_test_id_use_case(walk_test_results_by_walk_test_id_request=walk_test_results_by_walk_test_id_request)
        print("walk_test_by_walk_test_id_domain_list" + walk_test_results_with_device_info_composition.__str__())
        return WalkTestResultsByWalkTestIdResponse(result = walk_test_results_with_device_info_composition)