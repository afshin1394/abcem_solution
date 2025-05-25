import json
from fastapi import Query

from aio_pika.abc import AbstractRobustConnection
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.infrastructure.di.controllers import get_sms_controller
from app.infrastructure.rabbit import get_rabbit
from app.interfaces.controllers.sms_controller import SmsController
from app.interfaces.dto.request.get_n_last_sms_records_request import GetNLastSmsRecordsRequest
from app.interfaces.dto.request.send_sms_request import SendSmsRequest
from app.interfaces.dto.response.get_n_last_sms_records_response import GetNLastSmsRecordsResponse
from app.interfaces.dto.response.send_sms_response import SendSmsResponse

router_v1 = APIRouter(
    prefix="/sms",
    tags=["sms"],
)
import uuid
import aio_pika

@router_v1.post("/send_sms", response_model=SendSmsResponse)
async def send_sms(send_sms_request: SendSmsRequest,sms_controller : SmsController = Depends(get_sms_controller)):
    return await sms_controller.send_sms(send_sms_request)
    # channel = await connection.channel(publisher_confirms=True)
    #
    # # Declare a temporary exclusive queue for the reply
    # callback_queue = await channel.declare_queue(exclusive=True)
    # correlation_id = str(uuid.uuid4())
    #
    # future = asyncio.get_event_loop().create_future()
    #
    # async def on_response(message: aio_pika.abc.AbstractIncomingMessage):
    #     if message.correlation_id == correlation_id:
    #         future.set_result(json.loads(message.body))
    #
    # await callback_queue.consume(on_response)
    #
    # message = aio_pika.Message(
    #     body=json.dumps(event_data).encode(),
    #     reply_to=callback_queue.name,
    #     correlation_id=correlation_id
    # )
    #
    # await channel.default_exchange.publish(
    #     message,
    #     routing_key=settings.sms_queue_name
    # )
    #
    # # Wait for the response
    # response = await asyncio.wait_for(future, timeout=10)
    #
    # await channel.close()
    # log.info(msg=f"send sms {message}")
    # return SendSmsResponse(status_code=201, result=response)


@router_v1.post("/flood_sms")
async def flood_sms(connection: AbstractRobustConnection = Depends(get_rabbit)):
    channel = await connection.channel(publisher_confirms=True)
    exchange = channel.default_exchange

    for i in range(100):
        message = aio_pika.Message(body=json.dumps({"id": i}).encode())
        await exchange.publish(
                message,
                routing_key=settings.sms_queue_name
            )

    await channel.close()
    return SendSmsResponse(status_code=201)

@router_v1.get("/records", response_model=GetNLastSmsRecordsResponse)
async def get_paginated_sms_records(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sms_controller: SmsController = Depends(get_sms_controller)
):
    n_last_sms_records_request = GetNLastSmsRecordsRequest(page= page ,page_size=limit)
    return await sms_controller.get_n_last_sms_records(n_last_sms_records_request=n_last_sms_records_request)