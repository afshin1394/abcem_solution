from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain
from app.domain.repositories.read.read_speed_test_server_repository import ReadSpeedTestServerRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_speed_test_servers import TableSpeedTestServer


class ReadSpeedTestServerRepositoryImpl(ReadSpeedTestServerRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[SpeedTestServerDomain]:
        result = await self.db.execute(
            select(TableSpeedTestServer).where(TableSpeedTestServer.country == 'Iran').order_by(TableSpeedTestServer.id.asc())
        )
        records = result.scalars().all()
        servers_domain_list = await map_models_list(records, SpeedTestServerDomain)

        return servers_domain_list
