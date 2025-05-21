from fastapi.security import api_key

from app.application.usecase.base_use_case import BaseUseCase
from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.exceptions import RequestHeaderUnavailable, AccessTokenExpiredException
from app.domain.services.token_service import TokenService


class ValidateAccessTokenUseCase(BaseUseCase):
    def __init__(self, token_service: TokenService, api_key: str,cache : CacheGateway ):
        self.token_service = token_service
        self.api_key = api_key  # Store API key from header
        self.cache = cache

    async def execute(self) -> str:
        # Validate API Key
        print("api_key",api_key)
        if not self.api_key.startswith("Bearer "):
            raise RequestHeaderUnavailable()
        print("api_key",api_key)

        # Extract token from header
        access_token = self.api_key.split("Bearer ")[1]

        if await self.cache.sys_member(settings.blacklisted_tokens_set, access_token):
            raise AccessTokenExpiredException()
        # Validate token
        if not self.token_service.validate_access_token(access_token):
            raise AccessTokenExpiredException()

        return access_token  # ✅ Return token if valid