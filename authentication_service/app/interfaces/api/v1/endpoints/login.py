from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers.auth_controller import get_auth_controller
from app.infrastructure.di.redis_client import get_redis_instance
from app.infrastructure.logto import fetch_access_token
from app.infrastructure.redis import RedisClient
from app.interfaces.controller.auth_controller import AuthController
from app.interfaces.dto.request.login_request_dto import LoginRequestDto
from app.interfaces.dto.request.verify_request_dto import VerifyRequestDTO
from app.interfaces.dto.response.login_response_dto import LoginResponseDTO
from app.interfaces.dto.response.verify_response_dto import VerifyResponseDTO

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponseDTO)
async def login(login_request: LoginRequestDto,
                auth_controller: AuthController = Depends(get_auth_controller)) -> LoginResponseDTO:
    return await auth_controller.login(login_dto=login_request)


@router.post("/verify", response_model=VerifyResponseDTO)
async def verify(verify_request: VerifyRequestDTO,
                 auth_controller: AuthController = Depends(get_auth_controller)) -> VerifyResponseDTO:
    return await auth_controller.verify(verify_request)


@router.get("/test_redis")
async def validate_location(redis_client: RedisClient = Depends(get_redis_instance)):
    await redis_client.set("test", "1")
    return await redis_client.redis.get("test")

# Define a FastAPI endpoint for testing
@router.post("/get-access-token")
async def get_access_token():
    access_token = await fetch_access_token()
    return {"access_token": access_token}
