import asyncio
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection

from app.core.config import settings


class RateLimitedConsumer:
    def __init__(self,  connection: AbstractRobustConnection,max_event_per_second : int, event_handler: callable = None):
        self.connection = connection
        self.channel = None
        self.queue = None
        self.max_event_per_second = max_event_per_second
        self.token_bucket = asyncio.Semaphore(max_event_per_second)
        self.event_handler = event_handler

    async def start(self):
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.max_event_per_second)
        self.queue = await self.channel.declare_queue("sms_queue", durable=True,arguments={
                "x-dead-letter-exchange": "dlx",    # Failed messages will go here
                "x-dead-letter-routing-key": "dlq", # Use this routing key for DLQ
            },)
        # Start consuming messages
        await self.queue.consume(callback= self.process_message_wrapper)

        # Start refilling the token bucket every second
        asyncio.create_task(self.refill_tokens())




    async def refill_tokens(self):
        while True:
            await asyncio.sleep(1)
            for _ in range(10 - self.token_bucket._value):
                self.token_bucket.release()

    async def process_message_wrapper(self, message: AbstractIncomingMessage):
        await self.token_bucket.acquire()
        retry_count = message.headers.get("x-retry-count", 0)

        async with message.process(requeue=True):
            try:
                event = json.loads(message.body)
                result = await self.event_handler(event)  # Optional: event handler can return a result

                # If it's an RPC call, reply to the producer
                if message.reply_to and message.correlation_id:
                    response_body = json.dumps({"status": "processed", "details": result}).encode()
                    await self.channel.default_exchange.publish(
                        aio_pika.Message(
                            body=response_body,
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )

            except json.JSONDecodeError:
                print(f"Bad message format: {message.body}")
                await message.reject(requeue=False)
            except Exception as e:
                print(f"Error processing message: {e}")
                if retry_count >= settings.rabbit_message_retry_count:
                    print("Max retries exceeded, rejecting message...")
                    await message.reject(requeue=False)
                else:
                    await self.republish_with_retry_count(message, retry_count + 1)
                    await message.ack()

    async def republish_with_retry_count(self, message: AbstractIncomingMessage, retry_count: int):
        new_message = aio_pika.Message(
            body=message.body,
            headers={"x-retry-count": retry_count},
            reply_to=message.reply_to,
            correlation_id=message.correlation_id
        )
        await self.channel.default_exchange.publish(
            new_message,
            routing_key=self.queue.name
        )
