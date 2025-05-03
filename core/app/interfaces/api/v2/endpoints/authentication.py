from fastapi import  APIRouter


router_v2 = APIRouter(
    prefix="/authentication",
    tags=["authentication"],
)


@router_v2.get("/login")
def login():
    return [{"login": "true"}]

@router_v2.get("/verify")
def verify():
    return [{"verify": "true"}]