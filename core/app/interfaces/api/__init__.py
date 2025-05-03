from fastapi import APIRouter

from app.interfaces.api.v1 import router_v1 as v1
from app.interfaces.api.v2 import router_v2  as v2

router_all = APIRouter()

router_all.include_router(v1)
router_all.include_router(v2)
