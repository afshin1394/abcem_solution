from fastapi import APIRouter, Depends

from app.infrastructure.di.api_key_header import get_validate_token
from app.infrastructure.di.controllers import get_walk_test_results_controller, get_device_info_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.device_info_controller import DeviceInfoController
from app.interfaces.controllers.walk_test_results_controller import WalkTestResultsController
from app.interfaces.dto.request.update_device_info_request import UpdateDeviceInfoRequest
from app.interfaces.dto.request.walk_test_results_by_walk_test_id_request import WalkTestResultsByWalkTestIdRequest
from app.interfaces.dto.request.walk_test_results_request import WalkTestResultsRequest
from app.interfaces.dto.response.update_device_info_response import ReceiveDeviceInfoResponse
from app.interfaces.dto.response.walk_test_results_by_walk_test_id_response import WalkTestResultsByWalkTestIdResponse
from app.interfaces.dto.response.walk_test_results_response import WalkTestResultsResponse

router_walk_test_results = APIRouter()

router_public = APIRouter(prefix="/public/walk_test_results",tags=["walk_test_results"])
router_protected = APIRouter(prefix="/protected/walk_test_results",tags=["walk_test_results"],dependencies=[Depends(get_validate_token)])
router_private = APIRouter(prefix="/private/walk_test_results",tags=["walk_test_results"])



@router_protected.post("/send", response_model=WalkTestResultsResponse)
async def send_walk_test_results(walk_test_results_request: WalkTestResultsRequest,walk_test_controller: WalkTestResultsController = Depends(get_walk_test_results_controller)):
    return await walk_test_controller.receive_walk_test_results(walk_test_results_request)


@router_protected.post("/get_all_by_id", response_model=WalkTestResultsByWalkTestIdResponse,response_model_exclude_none=True)
async def get_walk_test_results_by_walk_test_id(walk_test_results_by_walk_test_id_request: WalkTestResultsByWalkTestIdRequest,walk_test_results_controller: WalkTestResultsController = Depends(get_walk_test_results_controller)):
    return await walk_test_results_controller.get_walk_test_results_by_walk_test_id(walk_test_results_by_walk_test_id_request=walk_test_results_by_walk_test_id_request)

@router_protected.put("/send_device_info", response_model = ReceiveDeviceInfoResponse)
async def update_device_info(update_device_info_request : UpdateDeviceInfoRequest, device_info_controller : DeviceInfoController = Depends(get_device_info_controller)) :
    return await device_info_controller.update_device_info(update_device_info_request = update_device_info_request)



router_walk_test_results.include_router(router_public)
router_walk_test_results.include_router(router_protected)
router_walk_test_results.include_router(router_private)