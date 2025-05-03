from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.device_info_domain import DeviceInfoDomain
from app.domain.repositories.read.read_device_info_repository import ReadDeviceInfoRepository
from app.infrastructure.mapper.mapper import map_models
from app.infrastructure.schemas.table_device_info import TableDeviceInfo


class ReadDeviceInfoRepositoryImpl(ReadDeviceInfoRepository):


    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_device_info_by_walk_test_id(self, walk_test_id: str) -> DeviceInfoDomain:
        result = await self.db.execute(
            select(TableDeviceInfo).where(TableDeviceInfo.walk_test_id == walk_test_id)
        )
        device_info_schema = result.scalar_one_or_none()
        print("device_info_schema" + device_info_schema.__str__())
        device_info_domain = await map_models(device_info_schema, DeviceInfoDomain)
        return device_info_domain