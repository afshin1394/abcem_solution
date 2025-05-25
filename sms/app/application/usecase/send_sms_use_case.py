import asyncio
import json
import logging
import uuid

import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.application.feature.commands.insert_sms_command import InsertSmsCommand
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.core.config import settings
from app.interfaces.dto.request.send_sms_request import SendSmsRequest


class SendSmsUseCase(BaseUseCase):

    def __init__(self, mediator: Mediator,connection: AbstractRobustConnection , log: logging.Logger) -> None:
        self.mediator = mediator
        self.connection = connection
        self.log = log


    async def execute(self,**kwargs) -> str:
        send_sms_request : SendSmsRequest = kwargs.get("send_sms_request")
        print(f"send_sms_request {send_sms_request}",flush=True)

        correlation_id = str(uuid.uuid4())

        insert_sms_command = InsertSmsCommand(correlation_id=correlation_id,phone_number=send_sms_request.phone_number,message=send_sms_request.message)
        print(f"insert_sms_command {insert_sms_command}",flush=True)

        channel = await self.connection.channel(publisher_confirms=True)

        # Declare a temporary exclusive queue for the reply
        callback_queue = await channel.declare_queue(exclusive=True)

        future = asyncio.Future()

        async def on_response(message: aio_pika.abc.AbstractIncomingMessage):
            if message.correlation_id == correlation_id:
                future.set_result(json.loads(message.body))

        await callback_queue.consume(on_response)
        message = aio_pika.Message(
            body=insert_sms_command.model_dump_json().encode(),
            reply_to=callback_queue.name,
            correlation_id=correlation_id
        )

        await channel.default_exchange.publish(
            message,
            routing_key=settings.sms_queue_name
        )

        # Wait for the response
        response = await asyncio.wait_for(future, timeout=10)
        self.log.info(msg=f"response {response}")

        await channel.close()
        await self.mediator.send(insert_sms_command)
        # self.log.info(msg=f"send sms {message}")

        return "success"
