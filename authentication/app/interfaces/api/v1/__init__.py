from fastapi import APIRouter
from app.interfaces.api.v1.endpoints.auth import router_public
from app.interfaces.api.v1.endpoints.auth import router_private
from app.interfaces.api.v1.endpoints.auth import router_protected
router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(router_public)
router_v1.include_router(router_private)
router_v1.include_router(router_protected)
