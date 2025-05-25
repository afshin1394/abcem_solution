from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres_async import AsyncSessionLocal


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


