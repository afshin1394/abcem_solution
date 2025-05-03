from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.di import redis_client
from app.infrastructure.di.controllers import authentication_controller
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.speed_test import get_speed_test
from app.infrastructure.redis import RedisCacheGateway
from app.infrastructure.services_impl.speed_test_servers import Speedtest, SpeedtestException
from app.interfaces.controllers.authentication_controller import AuthenticationController

router_v1 = APIRouter(
    prefix="/validation",
    tags=["validation"]
)


@router_v1.get("/validate_ip")
async def get_ip_info(controller: AuthenticationController = Depends(authentication_controller)):
    pass
    # try:
    #     ip_info = await controller.authenticate(authenticate_request= AuthenticationRequest())
    #     return ip_info
    # except httpx.HTTPStatusError as e:
    #     # Handle specific HTTP errors
    #     raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    # except httpx.RequestError as e:
    #     # Handle network-related errors
    #     raise HTTPException(status_code=500, detail=str(e))
    # except Exception as e:
    #     # Handle any other unexpected errors
    #     raise HTTPException(status_code=500, detail=str(e))
    # implement in other service


@router_v1.post("/test_redis")
async def validate_location(
        key: str,
        value: str,
        redis_client: RedisCacheGateway = Depends(get_cache)):
    await redis_client.set(key, value)
    return await redis_client.get(key)

@router_v1.delete("/test_delete_redis")
async def delete_redis(
        key: str,
        redis_client: RedisCacheGateway = Depends(get_cache)):
    await redis_client.invalidate_keys(keys= [key])
    return {"message": f"Key '{key}' invalidated"}
@router_v1.get("/get_value_redis")
async def get_value_redis(
    key: str,
    redis_client: RedisCacheGateway = Depends(get_cache)
):
    return await redis_client.get(key)
