from fastapi import APIRouter


router_v2 = APIRouter(
    prefix="/validation",
    tags=["validation"],
)


@router_v2.get("/validate_ip")
def get_ip_info():
    return ["true"]




