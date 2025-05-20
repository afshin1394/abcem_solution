from fastapi import APIRouter, Depends, Header

from app.infrastructure.di.api_key_header import get_bearer_token
from app.infrastructure.di.controllers.auth_controller import get_auth_controller
from app.infrastructure.di.usecases.validate_token_use_case import get_validate_token_use_case
from app.interfaces.controller.auth_controller import AuthController
from app.interfaces.dto.request.login_request_dto import LoginRequestDto
from app.interfaces.dto.request.logout_request import LogoutRequest
from app.interfaces.dto.request.refresh_token_request_dto import RefreshTokenRequest
from app.interfaces.dto.request.verify_request_dto import VerifyRequestDTO
from app.interfaces.dto.response.login_response import LoginResponse
from app.interfaces.dto.response.refresh_token_response import RefreshTokenResponse
from app.interfaces.dto.response.verify_response import VerifyResponse

router_public = APIRouter(prefix="/auth/public",tags=["authentication"])
router_protected = APIRouter(prefix="/auth/protected",tags=["authentication"],dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/auth/private",tags=["authentication"])


@router_public.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequestDto,
                auth_controller: AuthController = Depends(get_auth_controller)) -> LoginResponse:
    print("auth_controller",auth_controller)
    return await auth_controller.login(login_dto=login_request)


@router_public.post("/verify", response_model=VerifyResponse)
async def verify(verify_request: VerifyRequestDTO,
                 auth_controller: AuthController = Depends(get_auth_controller)) -> VerifyResponse:
    return await auth_controller.verify(verify_request)


@router_public.post("/refresh", response_model= RefreshTokenResponse)
async def refresh_access_token(refresh_token_request: RefreshTokenRequest,
                 auth_controller: AuthController = Depends(get_auth_controller)) -> RefreshTokenResponse:
    return await auth_controller.refresh_token(refresh_token_request)


@router_protected.post("/logout")
async def logout(logout_request: LogoutRequest,auth_controller: AuthController = Depends(get_auth_controller),access_token: str = Depends(get_bearer_token)):
    print("access_token",access_token)
    return await auth_controller.logout(logout_request=logout_request,access_token= access_token)


