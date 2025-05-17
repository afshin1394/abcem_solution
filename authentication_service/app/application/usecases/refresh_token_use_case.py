from typing import Any

from app.application.services.token_service import TokenService
from app.application.usecases.base_use_case import BaseUseCase
from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.token_domain import TokenDomain
from app.domain.exceptions import RefreshTokenExpiredException, FailAddingToBlacklistException


class RefreshTokenUseCase(BaseUseCase):


    def __init__(self, token_service: TokenService,cache_gateway: CacheGateway):
        self.token_service = token_service
        self.cache_gateway = cache_gateway

    async def execute(self, refresh_token: str) -> TokenDomain:
        if not await self.token_service.validate_refresh_token(refresh_token):
            raise RefreshTokenExpiredException()

        if await self.cache_gateway.sys_member(settings.blacklisted_tokens_set,refresh_token):
            raise RefreshTokenExpiredException()

        added = await self.cache_gateway.sadd(settings.blacklisted_tokens_set, refresh_token)
        print("added",added)
        if added == 0:
            raise FailAddingToBlacklistException()

        return await self.token_service.generate_tokens_based_on_refresh_token(refresh_token)

