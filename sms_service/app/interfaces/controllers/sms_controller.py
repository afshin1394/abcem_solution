from fastapi import Depends

from app.application.usecase.get_n_last_sms_records_use_case import GetNLastSmsRecordsUseCase
from app.application.usecase.send_all_sms_use_case import SendAllSMSUseCase
from app.application.usecase.send_sms_use_case import SendSmsUseCase
from app.domain.entities import PaginatedResult
from app.domain.entities.sms_record_domain import SMSRecordDomain

from app.interfaces.dto.request.get_n_last_sms_records_request import GetNLastSmsRecordsRequest
from app.interfaces.dto.request.send_sms_request import SendSmsRequest
from app.interfaces.dto.response.get_n_last_sms_records_response import GetNLastSmsRecordsResponse
from app.interfaces.dto.response.send_sms_response import SendSmsResponse


class SmsController:



    def __init__(self,n_last_sms_records_use_case : GetNLastSmsRecordsUseCase,
                 send_sms_use_case : SendSmsUseCase,
                 send_all_sms_use_case : SendAllSMSUseCase):
        super().__init__()
        self.n_last_sms_records_use_case = n_last_sms_records_use_case
        self.send_sms_use_case = send_sms_use_case
        self.send_all_sms_use_case = send_all_sms_use_case

    async def get_n_last_sms_records(self,n_last_sms_records_request : GetNLastSmsRecordsRequest) ->  GetNLastSmsRecordsResponse:
      result  = await self.n_last_sms_records_use_case.execute(n_last_sms_records_request=n_last_sms_records_request)
      print(f"result PaginatedResult {result}",flush=True)
      return GetNLastSmsRecordsResponse(result=result.items,page=result.page,page_size=result.page_size,total_items=result.total_items)


    async def send_sms(self,send_sms_request : SendSmsRequest) -> SendSmsResponse:
        result  = await self.send_sms_use_case.execute(send_sms_request=send_sms_request)
        print(f"send_sms result {result}",flush=True)
        return SendSmsResponse(result=result)

    async def send_all_sms(self, send_sms_request_list: list[SendSmsRequest]) -> SendSmsResponse:

        result = await self.send_all_sms_use_case.execute(send_sms_request_list = send_sms_request_list)

        return SendSmsResponse(result=result)