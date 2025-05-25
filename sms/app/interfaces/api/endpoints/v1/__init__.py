from fastapi import APIRouter

from app.interfaces.api.endpoints.v1.sms import router_v1 as sms_router

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(sms_router)

