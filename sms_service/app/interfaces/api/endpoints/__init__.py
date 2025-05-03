from fastapi import APIRouter

from app.interfaces.api.endpoints.v1.sms import router_v1 as v1
from app.interfaces.api.endpoints.v2.sms import router_v2  as v2

router_all = APIRouter()

router_all.include_router(v1)
router_all.include_router(v2)
