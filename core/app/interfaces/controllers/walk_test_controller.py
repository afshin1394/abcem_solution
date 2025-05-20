

from app.application.usecase.create_walk_test_usecase import CreateWalkTestUseCase
from app.application.usecase.get_all_walk_test_by_msisdn_usecase import GetAllWalkTestByMSISDNUseCase
from app.application.usecase.get_walk_test_results_by_walk_test_id_use_case import GetWalkTestResultsByWalkTestIdUseCase
from app.application.usecase.insert_walk_test_results_use_case import InsertWalkTestResultsUseCase
from app.application.usecase.update_walk_test_status_use_case import UpdateWalkTestStatusUseCase
from app.application.usecase.validate_walk_test_process_usecase import ValidateWalkTestProcessUseCase

from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.request.get_walk_test_by_msisdn_request import GetWalkTestByMSISDNRequest
from app.interfaces.dto.request.update_walk_test_status_request import UpdateWalkTestStatusRequest
from app.interfaces.dto.request.validate_walk_test_process_request import ValidateWalkTestProcessRequest
from app.interfaces.dto.request.walk_test_request import WalkTestRequest
from app.interfaces.dto.response.update_walk_test_status_response import UpdateWalkTestStatusResponse
from app.interfaces.dto.response.validate_walk_test_process_response import ValidateWalkTestProcessResponse
from app.interfaces.dto.response.walk_test_by_msisdn_response import WalkTestByMSISDNResponse, WalkTestByMSISDN
from app.interfaces.dto.response.walk_test_created_response import WalkTestCreatedResponse


class WalkTestController:
    def __init__(self, create_walk_test_use_case: CreateWalkTestUseCase,
                 get_all_walk_test_by_msisdn_use_case: GetAllWalkTestByMSISDNUseCase,
                 update_walk_test_status_use_case: UpdateWalkTestStatusUseCase,
                 validate_walk_test_process_use_case : ValidateWalkTestProcessUseCase,
                 ):

        self.create_walk_test_use_case = create_walk_test_use_case
        self.get_all_walk_test_by_msisdn_use_case = get_all_walk_test_by_msisdn_use_case
        self.update_walk_test_status_use_case = update_walk_test_status_use_case
        self.validate_walk_test_process_use_case = validate_walk_test_process_use_case

    async def create_walk_test(self, walk_test_request: WalkTestRequest) -> WalkTestCreatedResponse:
        walk_test_data = await self.create_walk_test_use_case(
            create_walk_test_request=walk_test_request
        )

        # 2. Pass 'walk_test_data' into the model's 'result' field
        response = WalkTestCreatedResponse(status_code = 201,result=walk_test_data)
        print("response" + response.result)

        return response

    async def get_walk_test_by_msisdn(self,
                                      walk_test_by_msisdn_request: GetWalkTestByMSISDNRequest) -> WalkTestByMSISDNResponse:
        walk_test_by_msisdn_domain_list = await self.get_all_walk_test_by_msisdn_use_case(
            get_walk_test_by_msisdn_request=walk_test_by_msisdn_request)
        response_list = await map_models_list(walk_test_by_msisdn_domain_list, WalkTestByMSISDN)
        print("response" + response_list.__str__())
        return WalkTestByMSISDNResponse(result=response_list)




    async def update_walk_test_status(self,update_walk_test_status_request : UpdateWalkTestStatusRequest) -> UpdateWalkTestStatusResponse:
        await self.update_walk_test_status_use_case(update_walk_test_status_request=update_walk_test_status_request)
        return UpdateWalkTestStatusResponse(status_code = 204,result= None)

    async def validate_walk_test_process(self,
                                      validate_walk_test_process_request: ValidateWalkTestProcessRequest) -> ValidateWalkTestProcessResponse:
        is_validated = await self.validate_walk_test_process_use_case(validate_walk_test_process_request=validate_walk_test_process_request)
        return ValidateWalkTestProcessResponse(result=is_validated)