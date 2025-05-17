from app.application.services.token_service import TokenService
from app.application.usecases.verify_use_case import VerifyUseCase
from fastapi import Depends

from app.domain.cache.cache_gateway import CacheGateway
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.services.token_service import get_token_service


async def get_verify_use_case(cache_gateway: CacheGateway = Depends(get_cache), token_service: TokenService = Depends(get_token_service)):
    return VerifyUseCase(cache_gateway=cache_gateway, token_service=token_service)
