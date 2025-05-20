from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.application.services.token_service import TokenService
from app.application.usecases.validate_token_use_case import ValidateAccessTokenUseCase
from app.domain.cache.cache_gateway import CacheGateway
from app.infrastructure.di.api_key_header import security
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.services.token_service import get_token_service


async def get_validate_token_use_case(
    token_service: TokenService = Depends(get_token_service),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    cache_gateway : CacheGateway = Depends(get_cache),
):
    access_token = credentials.credentials  # Gets only the token, not "Bearer "
    return ValidateAccessTokenUseCase(token_service=token_service, api_key=access_token,cache=cache_gateway)

