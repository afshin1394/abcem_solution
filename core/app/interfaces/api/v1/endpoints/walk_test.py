

from fastapi import APIRouter, Depends


from app.infrastructure.di.controllers import get_walk_test_controller
from app.interfaces.controllers.walk_test_controller import WalkTestController
from app.interfaces.dto.request.get_walk_test_by_msisdn_request import GetWalkTestByMSISDNRequest
from app.interfaces.dto.request.update_walk_test_status_request import UpdateWalkTestStatusRequest
from app.interfaces.dto.request.validate_walk_test_process_request import ValidateWalkTestProcessRequest
from app.interfaces.dto.request.walk_test_request import WalkTestRequest
from app.interfaces.dto.request.walk_test_results_by_walk_test_id_request import WalkTestResultsByWalkTestIdRequest
from app.interfaces.dto.request.walk_test_results_request import WalkTestResultsRequest
from app.interfaces.dto.response.update_walk_test_status_response import UpdateWalkTestStatusResponse
from app.interfaces.dto.response.validate_walk_test_process_response import ValidateWalkTestProcessResponse
from app.interfaces.dto.response.walk_test_by_msisdn_response import WalkTestByMSISDNResponse
from app.interfaces.dto.response.walk_test_created_response import WalkTestCreatedResponse
from app.interfaces.dto.response.walk_test_results_by_walk_test_id_response import WalkTestResultsByWalkTestIdResponse
from app.interfaces.dto.response.walk_test_results_response import WalkTestResultsResponse

router_v1 = APIRouter(
    prefix="/walk_test",
    tags=["walk_test"]
)


@router_v1.post("/create", response_model=WalkTestCreatedResponse)
async def create(walk_test_request: WalkTestRequest,
                 walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    walk_test_created_response = await walk_test_controller.create_walk_test(walk_test_request)


    return walk_test_created_response

@router_v1.post("/get_all", response_model=WalkTestByMSISDNResponse)
async def get_all_by_msisdn(walk_test_by_msisdn_request: GetWalkTestByMSISDNRequest,
                            walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.get_walk_test_by_msisdn(walk_test_by_msisdn_request=walk_test_by_msisdn_request)
@router_v1.post("/send_walk_test_results", response_model=WalkTestResultsResponse)
async def send_walk_test_results(walk_test_results_request: WalkTestResultsRequest,walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.receive_walk_test_results(walk_test_results_request)

@router_v1.post("/get_walk_test_results_by_walk_test_id", response_model=WalkTestResultsByWalkTestIdResponse,response_model_exclude_none=True)
async def get_walk_test_results_by_walk_test_id(walk_test_results_by_walk_test_id_request: WalkTestResultsByWalkTestIdRequest,walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.get_walk_test_results_by_walk_test_id(walk_test_results_by_walk_test_id_request=walk_test_results_by_walk_test_id_request)

@router_v1.put("/update_walk_test_status", response_model=UpdateWalkTestStatusResponse,response_model_exclude_none=True)
async def get_walk_test_results_by_walk_test_id(update_walk_test_status_request: UpdateWalkTestStatusRequest,walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.update_walk_test_status(update_walk_test_status_request=update_walk_test_status_request)

@router_v1.post("/validate_walk_test_process", response_model=ValidateWalkTestProcessResponse,response_model_exclude_none=True)
async def validate_walk_test_process(validate_walk_test_process_request: ValidateWalkTestProcessRequest,walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.validate_walk_test_process(validate_walk_test_process_request=validate_walk_test_process_request)