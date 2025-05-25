from typing import Any

from app.application.feature.queries.get_n_last_sms_query import GetNLastSmsRecordsQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities import PaginatedResult
from app.domain.entities.sms_record_domain import SMSRecordDomain
from app.interfaces.dto.request.get_n_last_sms_records_request import GetNLastSmsRecordsRequest


class GetNLastSmsRecordsUseCase(BaseUseCase):




    def __init__(self,mediator : Mediator) -> None:
        self.mediator = mediator

    async def execute(self, **kwargs) -> PaginatedResult[SMSRecordDomain]:
        get_n_last_sms_records_request = kwargs.get("n_last_sms_records_request")
        if isinstance(get_n_last_sms_records_request, GetNLastSmsRecordsRequest):
          print("n_last_sms_records_request" + get_n_last_sms_records_request.__str__(),flush=True)
          get_n_last_sms_records_query = GetNLastSmsRecordsQuery(page =get_n_last_sms_records_request.page,page_size= get_n_last_sms_records_request.page_size)
          print(f"n_last_sms_records_request {get_n_last_sms_records_query}",flush=True)
          result = await self.mediator.send(get_n_last_sms_records_query)
          print(f"execute result {result}",flush=True)
          return result
        else:
          print("The argument is not of type 'n_last_sms_records_request'")