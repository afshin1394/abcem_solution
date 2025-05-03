from typing import Any

from app.application.feature.commands.update_device_info_command import UpdateDeviceInfoCommand
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.infrastructure.mapper.mapper import map_models
from app.interfaces.dto.request.update_device_info_request import UpdateDeviceInfoRequest


class UpdateDeviceInfoUseCase(BaseUseCase):


    def __init__(self,mediator : Mediator):
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> str:
        send_device_info_request = kwargs.get("update_device_info_request")
        if isinstance(send_device_info_request, UpdateDeviceInfoRequest):
            print("send_device_info_request" + send_device_info_request.__str__())
            send_device_info_command = await map_models(send_device_info_request, UpdateDeviceInfoCommand)
            return await self.mediator.send(send_device_info_command)
        else:
            print("The argument is not of type 'send_device_info_request'")
