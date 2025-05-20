from typing import Any

from app.application.services.token_service import TokenService
from app.application.usecases.base_use_case import BaseUseCase
from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.token_domain import TokenDomain
from app.domain.exceptions import RefreshTokenExpiredException
from app.infrastructure.exceptions import RedisSetException


class LogoutUseCase(BaseUseCase):

    def __init__(self, token_service: TokenService, cache_gateway : CacheGateway):
        self.token_service = token_service
        self.cache_gateway = cache_gateway

    async def execute(self,refresh_token : str,access_token : str) -> str:
        if not await self.token_service.validate_refresh_token(refresh_token):
            raise RefreshTokenExpiredException()

        if await self.cache_gateway.sys_member(settings.blacklisted_tokens_set,refresh_token):
            raise RefreshTokenExpiredException()


        try:
          await self.cache_gateway.sadd(settings.blacklisted_tokens_set, access_token)
        except:
            raise RedisSetException(key=settings.blacklisted_tokens_set)
        try:
          await self.cache_gateway.sadd(settings.blacklisted_tokens_set, refresh_token)
        except:
            raise RedisSetException(key=settings.blacklisted_tokens_set)


        return 'success'
