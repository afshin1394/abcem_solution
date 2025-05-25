
import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.core.config import settings


async def get_rabbit() -> AbstractRobustConnection:
    """
    Returns the asynchronous RabbitMQ connection and channel.
    """
    return await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,  # Default RabbitMQ port
        login=settings.rabbitmq_user,  # Credentials from docker-compose.yml
        password=settings.rabbitmq_password,
    )




