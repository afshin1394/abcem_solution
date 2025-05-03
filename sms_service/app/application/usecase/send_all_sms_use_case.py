from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase


class SendAllSMSUseCase(BaseUseCase):



    def __init__(self,mediator : Mediator):
        super().__init__()
        self.mediator = mediator

    async def execute(self,**kwargs) -> str:
        send_sms_request_list = kwargs.get("send_sms_request_list")
        return ""
