
from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_speed_test_servers_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.speed_test_controller import SpeedTestServerController
from app.interfaces.dto.request.update_speed_test_servers_request import UpdateSpeedTestServersRequest
from app.interfaces.dto.response.speed_test_server_response import SpeedTestsServersResponse
from app.interfaces.dto.success_response import BaseSuccessResponse

router_speed_test = APIRouter()


router_public = APIRouter(prefix="/public/speed_test",tags=["speed_test"])
router_protected = APIRouter(prefix="/protected/speed_test",tags=["speed_test"],dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/private/speed_test",tags=["speed_test"])

@router_private.post("/update_servers", response_model = BaseSuccessResponse)
async def update(update_speed_test_servers_request : UpdateSpeedTestServersRequest, speed_test_controller : SpeedTestServerController = Depends(get_speed_test_servers_controller)) :
    return await speed_test_controller.update_speed_test_servers(update_speed_test_server_request=update_speed_test_servers_request)

@router_protected.get("/get_all", response_model = SpeedTestsServersResponse)
async def get_all( speed_test_controller : SpeedTestServerController = Depends(get_speed_test_servers_controller)) :
    return await speed_test_controller.get_all_speed_test_servers()


router_speed_test.include_router(router_public)
router_speed_test.include_router(router_protected)
router_speed_test.include_router(router_private)
