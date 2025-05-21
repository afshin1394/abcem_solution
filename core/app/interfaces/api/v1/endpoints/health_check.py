from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.di.api_key_header import get_validate_token
from app.infrastructure.di.database import get_db
router_health_check = APIRouter()

router_public = APIRouter(prefix="/public/health",tags=["health"])
router_protected = APIRouter(prefix="/protected/health",tags=["health"],dependencies=[Depends(get_validate_token)])
router_private = APIRouter(prefix="/private/health",tags=["health"])

@router_private.get("/check_data_base", response_model=None)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute('SELECT id FROM table_speed_test_servers')
        return {"status": "ok"}
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database not ready")

router_health_check.include_router(router_public)
router_health_check.include_router(router_protected)
router_health_check.include_router(router_private)