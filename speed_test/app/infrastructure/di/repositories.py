from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.write.single.write_speed_test_server_repository import WriteSpeedTestServerRepository
from app.infrastructure.di.database import get_db
from app.infrastructure.repository_impl.write.single.write_speed_test_server_repository_impl import  WriteSpeedTestServerRepositoryImpl


async def get_write_speed_test_server_repository(
        async_session: AsyncSession = Depends(get_db),
) -> WriteSpeedTestServerRepository:
    return WriteSpeedTestServerRepositoryImpl(db=async_session)