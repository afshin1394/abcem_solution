from fastapi import APIRouter

from app.interfaces.api.v1 import router_v1
from app.interfaces.api.v2 import router_v2


router = APIRouter(prefix="/api")
router.include_router(router_v1)
router.include_router(router_v2)
