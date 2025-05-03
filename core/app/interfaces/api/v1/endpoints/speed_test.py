
from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_speed_test_servers_controller
from app.interfaces.controllers.speed_test_controller import SpeedTestServerController
from app.interfaces.dto.request.update_speed_test_servers_request import UpdateSpeedTestServersRequest
from app.interfaces.dto.response.speed_test_server_response import SpeedTestsServersResponse
from app.interfaces.dto.success_response import BaseSuccessResponse

router_v1 = APIRouter(
    prefix="/speed_test",
    tags=["speed_test"],
)

@router_v1.post("/update_servers", response_model = BaseSuccessResponse)
async def update(update_speed_test_servers_request : UpdateSpeedTestServersRequest, speed_test_controller : SpeedTestServerController = Depends(get_speed_test_servers_controller)) :
    return await speed_test_controller.update_speed_test_servers(update_speed_test_server_request=update_speed_test_servers_request)
@router_v1.get("/get_all", response_model = SpeedTestsServersResponse)
async def get_all( speed_test_controller : SpeedTestServerController = Depends(get_speed_test_servers_controller)) :
    return await speed_test_controller.get_all_speed_test_servers()
