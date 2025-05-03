from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(url= settings.database_url)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db() -> Session:
    async with SyncSessionLocal() as session:
        yield session