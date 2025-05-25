from sqlalchemy import  func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.domain.entities.speed_test_server_domain import  SpeedTestServerDomain
from app.domain.repositories.write.single.write_speed_test_server_repository import WriteSpeedTestServerRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.repository_impl.write import BaseWriteDB
from app.infrastructure.schemas.table_speed_test_servers import TableSpeedTestServer


class WriteSpeedTestServerRepositoryImpl(BaseWriteDB,WriteSpeedTestServerRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def update_all(self, servers: list[SpeedTestServerDomain]):
       async with self:
         db_result = await map_models_list(servers, TableSpeedTestServer)
         db_rows = [
             {
                 col.name: getattr(instance, col.name)
                 for col in TableSpeedTestServer.__table__.columns
             }
             for instance in db_result
         ]

         stmt = insert(TableSpeedTestServer).values(db_rows)

         # Define what to update if conflict on server_id
         stmt = stmt.on_conflict_do_update(
             index_elements=["id"],  # id must be unique in DB
             set_={
                 "name": stmt.excluded.name,
                 "sponsor": stmt.excluded.sponsor,
                 "host": stmt.excluded.host,
                 "country": stmt.excluded.country,
                 "lat": stmt.excluded.lat,
                 "lon": stmt.excluded.lon,
                 "distance": stmt.excluded.distance,
                 "updated_at": func.now(),  # update timestamp
             },
         )

         await self.db.execute(stmt)
