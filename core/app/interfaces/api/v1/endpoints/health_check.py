from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.di.database import get_db

router_v1 = APIRouter(
    prefix="/health",
    tags=["health"],
)
@router_v1.get("/check_data_base", response_model=None)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute('SELECT id FROM table_speed_test_servers')
        return {"status": "ok"}
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database not ready")