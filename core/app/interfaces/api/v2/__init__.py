from fastapi import APIRouter

from app.interfaces.api.v2.endpoints.validation import router_v2 as validation_router
from app.interfaces.api.v2.endpoints.authentication import router_v2 as authentication_router

router_v2 = APIRouter(prefix="/v2")

router_v2.include_router(validation_router)
router_v2.include_router(authentication_router)