from app.application.usecase.update_device_info_usecase import UpdateDeviceInfoUseCase
from app.interfaces.dto.request.update_device_info_request import UpdateDeviceInfoRequest
from app.interfaces.dto.response.update_device_info_response import ReceiveDeviceInfoResponse


class DeviceInfoController:
    def __init__(self,update_device_info_use_case : UpdateDeviceInfoUseCase):
        self.update_device_info_use_case = update_device_info_use_case

    async def update_device_info(self,update_device_info_request : UpdateDeviceInfoRequest ) -> str:
      result = await self.update_device_info_use_case(update_device_info_request=update_device_info_request)
      return ReceiveDeviceInfoResponse(status_code = 201,result= result)
