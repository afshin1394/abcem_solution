# units of work
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repository.read.read_sms_repository import ReadSmsRepository
from app.domain.repository.write.write_sms_repository import WriteSmsRepository
from app.infrastructure.di.database import get_db
from app.infrastructure.repository_impl.read.read_sms_repository_impl import ReadSmsRepositoryImpl
from app.infrastructure.repository_impl.write.write_sms_repository_impl import WriteSmsRepositoryImpl


async def get_read_sms_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadSmsRepository:
    return ReadSmsRepositoryImpl(db=async_session)

async def get_write_sms_repository(
        async_session: AsyncSession = Depends(get_db)
) -> WriteSmsRepository:
    return WriteSmsRepositoryImpl(db=async_session)
