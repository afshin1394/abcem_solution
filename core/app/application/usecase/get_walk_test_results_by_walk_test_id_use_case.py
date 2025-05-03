
from app.application.feature.queries.get_device_info_by_walk_test_id_query import GetDeviceInfoByWalkTestIdQuery
from app.application.feature.queries.get_walk_test_results_by_walk_test_id_query import GetWalkTestResultsByWalkTestIdQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.device_info_domain import DeviceInfoDomain
from app.domain.entities.walk_test_results_domain import WalkTestResultsDomain
from app.infrastructure.mapper.mapper import map_models, map_models_list
from app.interfaces.dto.request.walk_test_results_by_walk_test_id_request import WalkTestResultsByWalkTestIdRequest
from app.interfaces.dto.response.walk_test_results_by_walk_test_id_response import WalkTestResultsByWalkTestIdResponse, \
    WalkTestResultsWithDeviceInfoComposition, DeviceInfoByWalkTestId, WalkTestResultsByWalkTestId


class GetWalkTestResultsByWalkTestIdUseCase(BaseUseCase):


    def __init__(self,mediator : Mediator) -> None:
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> WalkTestResultsWithDeviceInfoComposition:
        walk_test_results_by_walk_test_id_request = kwargs.get("walk_test_results_by_walk_test_id_request")
        print("walk_test_results_by_walk_test_id_request"+walk_test_results_by_walk_test_id_request.__str__())
        if isinstance(walk_test_results_by_walk_test_id_request, WalkTestResultsByWalkTestIdRequest):
            walk_test_results_by_walk_test_id_query = await map_models(walk_test_results_by_walk_test_id_request, GetWalkTestResultsByWalkTestIdQuery)
            device_info_by_walk_test_id_query = await map_models(walk_test_results_by_walk_test_id_request, GetDeviceInfoByWalkTestIdQuery)
            print("walk_test_results_by_walk_test_id_query"+walk_test_results_by_walk_test_id_query.__str__())
            print("device_info_by_walk_test_id_query"+device_info_by_walk_test_id_query.__str__())
            walk_test_domain_results = await self.mediator.send(walk_test_results_by_walk_test_id_query)
            print("walk_test_domain_results"+walk_test_domain_results.__str__())
            device_info_domain_result = await self.mediator.send(device_info_by_walk_test_id_query)
            print("device_info_domain_result"+device_info_domain_result.__str__())


            print("isinstance", "isinstance(device_info_domain_result, DeviceInfoDomain)")
            device_info = await map_models(device_info_domain_result,DeviceInfoByWalkTestId)
            steps = await map_models_list(walk_test_domain_results,WalkTestResultsByWalkTestId)
            return  WalkTestResultsWithDeviceInfoComposition(device_info= device_info , steps=steps)


        else:
            print("The argument is not of type 'WalkTestResultsByWalkTestIdRequest'")


