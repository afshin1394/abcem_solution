from fastapi import Depends

from app.application.services.token_service import TokenService
from app.application.usecases.logout_token_use_case import LogoutUseCase
from app.domain.cache.cache_gateway import CacheGateway
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.services.token_service import get_token_service

async def get_logout_use_case(
        token_service: TokenService = Depends(get_token_service),
        cache_gateway: CacheGateway = Depends(get_cache)
) -> LogoutUseCase:
    return LogoutUseCase(token_service=token_service, cache_gateway=cache_gateway)