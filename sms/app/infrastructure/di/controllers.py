from fastapi.params import Depends

from app.application.usecase.get_n_last_sms_records_use_case import GetNLastSmsRecordsUseCase
from app.application.usecase.send_all_sms_use_case import SendAllSMSUseCase
from app.application.usecase.send_sms_use_case import SendSmsUseCase
from app.infrastructure.di.usecase import get_n_last_sms_records_use_case, get_send_sms_use_case, \
    get_send_all_sms_use_case
from app.interfaces.controllers.sms_controller import SmsController


async def get_sms_controller(n_last_sms_records_use_case : GetNLastSmsRecordsUseCase = Depends(get_n_last_sms_records_use_case),send_sms_use_case : SendSmsUseCase = Depends(get_send_sms_use_case),send_all_sms_use_case : SendAllSMSUseCase = Depends(get_send_all_sms_use_case)) -> SmsController:
    return SmsController(n_last_sms_records_use_case=n_last_sms_records_use_case,send_sms_use_case=send_sms_use_case,send_all_sms_use_case=send_all_sms_use_case )