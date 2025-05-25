from app.core.logger import CustomJsonFormatter
from app.infrastructure.redis import RedisCacheGateway
import logging


async def get_cache() -> RedisCacheGateway:
    return await RedisCacheGateway.get_instance()

async def get_logger() -> logging.Logger:
  # Set up root logger once
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = CustomJsonFormatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

