import logging

from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends

from app.application.mediator import Mediator
from app.application.usecase.get_n_last_sms_records_use_case import GetNLastSmsRecordsUseCase
from app.application.usecase.send_all_sms_use_case import SendAllSMSUseCase
from app.application.usecase.send_sms_use_case import SendSmsUseCase
from app.infrastructure.di import get_logger
from app.infrastructure.di.mediator import get_mediator
from app.infrastructure.rabbit import get_rabbit


async def get_n_last_sms_records_use_case(
        mediator: Mediator = Depends(get_mediator),
) -> GetNLastSmsRecordsUseCase:
    return GetNLastSmsRecordsUseCase(mediator=mediator)

async def get_send_sms_use_case(
        mediator: Mediator = Depends(get_mediator),
        connection: AbstractRobustConnection =Depends(get_rabbit) ,
        log: logging.Logger = Depends(get_logger)
) -> SendSmsUseCase:
    return SendSmsUseCase(mediator=mediator,connection=connection,log=log)

async def get_send_all_sms_use_case(
        mediator: Mediator = Depends(get_mediator),
) -> SendAllSMSUseCase:
    return SendAllSMSUseCase(mediator=mediator)