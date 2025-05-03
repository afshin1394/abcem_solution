from app.application.services.token_service import TokenService
from app.application.usecases.refresh_token_use_case import RefreshTokenUseCase
from fastapi import Depends

from app.infrastructure.di.services.token_service import get_token_service


async def get_refresh_token_use_case(token_service : TokenService = Depends(get_token_service)):
    return RefreshTokenUseCase(token_service= token_service)