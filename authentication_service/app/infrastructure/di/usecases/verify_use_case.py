from app.application.repository.auth_repository import AuthRepository
from app.application.services.token_service import TokenService
from app.application.usecases.verify_use_case import VerifyUseCase
from fastapi import Depends

from app.infrastructure.di.repositries.auth_repository import get_auth_repository
from app.infrastructure.di.services.token_service import get_token_service


async def get_verify_use_case(auth_repository: AuthRepository = Depends(get_auth_repository), token_service: TokenService = Depends(get_token_service)):
    return VerifyUseCase(auth_repository=auth_repository, token_service=token_service)
