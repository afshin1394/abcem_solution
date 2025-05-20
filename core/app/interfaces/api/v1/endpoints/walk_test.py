

from fastapi import APIRouter, Depends


from app.infrastructure.di.controllers import get_walk_test_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.walk_test_controller import WalkTestController
from app.interfaces.dto.request.get_walk_test_by_msisdn_request import GetWalkTestByMSISDNRequest
from app.interfaces.dto.request.update_walk_test_status_request import UpdateWalkTestStatusRequest
from app.interfaces.dto.request.validate_walk_test_process_request import ValidateWalkTestProcessRequest
from app.interfaces.dto.request.walk_test_request import WalkTestRequest
from app.interfaces.dto.response.update_walk_test_status_response import UpdateWalkTestStatusResponse
from app.interfaces.dto.response.validate_walk_test_process_response import ValidateWalkTestProcessResponse
from app.interfaces.dto.response.walk_test_by_msisdn_response import WalkTestByMSISDNResponse
from app.interfaces.dto.response.walk_test_created_response import WalkTestCreatedResponse


router_walk_test = APIRouter()

router_public = APIRouter(prefix="/public/walk_test",tags=["walk_test"])
router_protected = APIRouter(prefix="/protected/walk_test",tags=["walk_test"],dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/private/walk_test",tags=["walk_test"])

@router_protected.post("/create", response_model=WalkTestCreatedResponse)
async def create(walk_test_request: WalkTestRequest,
                 walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    walk_test_created_response = await walk_test_controller.create_walk_test(walk_test_request)


    return walk_test_created_response

@router_protected.post("/get_all", response_model=WalkTestByMSISDNResponse)
async def get_all_by_msisdn(walk_test_by_msisdn_request: GetWalkTestByMSISDNRequest,
                            walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.get_walk_test_by_msisdn(walk_test_by_msisdn_request=walk_test_by_msisdn_request)

@router_protected.put("/update_walk_test_status", response_model=UpdateWalkTestStatusResponse,response_model_exclude_none=True)
async def get_walk_test_results_by_walk_test_id(update_walk_test_status_request: UpdateWalkTestStatusRequest,walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.update_walk_test_status(update_walk_test_status_request=update_walk_test_status_request)

@router_protected.post("/validate_walk_test_process", response_model=ValidateWalkTestProcessResponse,response_model_exclude_none=True)
async def validate_walk_test_process(validate_walk_test_process_request: ValidateWalkTestProcessRequest,walk_test_controller: WalkTestController = Depends(get_walk_test_controller)):
    return await walk_test_controller.validate_walk_test_process(validate_walk_test_process_request=validate_walk_test_process_request)



router_walk_test.include_router(router_public)
router_walk_test.include_router(router_private)
router_walk_test.include_router(router_protected)