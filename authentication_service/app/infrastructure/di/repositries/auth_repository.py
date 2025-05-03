from app.infrastructure.di.redis_client import get_redis_instance
from app.infrastructure.redis import RedisClient
from app.infrastructure.repository_impl.auth_repository_impl import AuthRepositoryImpl
from fastapi import Depends

async def get_auth_repository(redis_client : RedisClient = Depends(get_redis_instance)):
    return AuthRepositoryImpl(redis_client= redis_client)