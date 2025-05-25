
from app.application.services.token_service import TokenService
from app.application.usecases.base_use_case import BaseUseCase
from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.exceptions import RequestHeaderUnavailable, AccessTokenExpiredException

class ValidateAccessTokenUseCase(BaseUseCase):
    def __init__(self, token_service: TokenService, api_key: str,cache : CacheGateway ):
        self.token_service = token_service
        self.api_key = api_key  # Store API key from header
        self.cache = cache

    async def execute(self) -> str:
        # Validate API Key
        print("validate access token")
        if not self.api_key.startswith("Bearer "):
            raise RequestHeaderUnavailable()

        # Extract token from header
        access_token = self.api_key.split("Bearer ")[1]
        print("validate access token",access_token)

        if await self.cache.sys_member(settings.blacklisted_tokens_set, access_token):
            raise AccessTokenExpiredException()
        # Validate token
        print("access token ds dsdds", self.token_service.validate_access_token(access_token))

        if not await self.token_service.validate_access_token(access_token):
            raise AccessTokenExpiredException()

        return access_token  # ✅ Return token if valid