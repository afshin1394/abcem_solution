from fastapi import APIRouter, Depends

from app.core.config import settings
from app.infrastructure.di.controllers.auth_controller import get_auth_controller
from app.infrastructure.di.redis_client import get_redis_instance
from app.infrastructure.logto.services import fetch_access_token, seed_roles_and_users, create_roles_logto, \
    create_resources_with_scopes
from app.infrastructure.logto.utils import load_json_part, load_seed_data
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

@router.post("/seed_logto")
async def create_users():
     users =  load_json_part(settings.logto_json_path,"users")
     access_token = await fetch_access_token()
     seed_data  = load_seed_data(filepath=settings.logto_json_path)

     print(f"load json part: {users}")
     print(f"access token: {access_token}")
     await seed_roles_and_users(access_token= access_token,seed_data= seed_data)
     return {"users": users}

@router.post("/create_resource")
async def create_resource():
    access_token = await fetch_access_token()

    resources = load_json_part(settings.logto_json_path, "resources")
    print(f"resources: {resources}")

    json = create_resources_with_scopes(access_token,resources)

    return json

@router.post("/create_roles")
async def create_roles():
    access_token = await fetch_access_token()

    roles = load_json_part(settings.logto_json_path, "roles")
    print(f"roles: {roles}")

    json = create_roles_logto(access_token,roles)

    return json

