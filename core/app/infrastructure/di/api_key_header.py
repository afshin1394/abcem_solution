from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.exceptions import RequestHeaderUnavailable, AccessTokenInvalidException
from app.domain.services.token_service import TokenService
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.services import get_token_service

security = HTTPBearer()




async def get_validate_token(credentials: HTTPAuthorizationCredentials = Depends(security),token_service : TokenService = Depends(get_token_service),cache : CacheGateway = Depends(get_cache)):
    # Validate API Key
    token = credentials.credentials

    print("validate access token",token)
    if not token:
        raise RequestHeaderUnavailable()

    # Extract token from header
    if await cache.sys_member(settings.blacklisted_tokens_set, token):
        raise AccessTokenInvalidException()

    # Validate token
    await token_service.validate_access_token(token)
