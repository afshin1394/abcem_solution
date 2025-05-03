from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_device_info_controller
from app.interfaces.controllers.device_info_controller import DeviceInfoController
from app.interfaces.dto.request.update_device_info_request import UpdateDeviceInfoRequest
from app.interfaces.dto.response.update_device_info_response import ReceiveDeviceInfoResponse

router_v1 = APIRouter(
    prefix="/device_info",
    tags=["device_info"],
)


@router_v1.put("/update", response_model = ReceiveDeviceInfoResponse)
async def update_device_info(update_device_info_request : UpdateDeviceInfoRequest, device_info_controller : DeviceInfoController = Depends(get_device_info_controller)) :
    return await device_info_controller.update_device_info(update_device_info_request = update_device_info_request)