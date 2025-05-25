from fastapi import APIRouter

router_v2 = APIRouter(
    prefix="/sms",
    tags=["sms"],
)