from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.write.single.write_device_info_repository import WriteDeviceInfoRepository
from app.infrastructure.repository_impl.write import BaseWriteDB
from app.infrastructure.schemas.table_device_info import TableDeviceInfo
from app.domain.entities.device_info_domain import DeviceInfoDomain
from sqlalchemy import select


class WriteDeviceInfoRepositoryImpl(BaseWriteDB, WriteDeviceInfoRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def update_device_info(self, device_info_domain: DeviceInfoDomain):
        stmt = select(TableDeviceInfo).where(
            TableDeviceInfo.walk_test_id == device_info_domain.walk_test_id
        )

        async with self:
            result = await self.db.execute(stmt)
            existing_device = result.scalar_one_or_none()

            if existing_device:
                # Update the existing device information
                existing_device.security_patch = device_info_domain.security_patch
                existing_device.sdk = device_info_domain.sdk
                existing_device.os_version = device_info_domain.os_version
                existing_device.brand = device_info_domain.brand
                existing_device.device = device_info_domain.device
                existing_device.hardware = device_info_domain.hardware
                existing_device.model = device_info_domain.model

                # Commit the transaction (this will automatically be handled by the context manager)
                return "updated"
            else:
                # If the device doesn't exist, create a new device record
                new_device = TableDeviceInfo(
                    walk_test_id=device_info_domain.walk_test_id,
                    security_patch=device_info_domain.security_patch,
                    sdk=device_info_domain.sdk,
                    os_version=device_info_domain.os_version,
                    brand=device_info_domain.brand,
                    device=device_info_domain.device,
                    hardware=device_info_domain.hardware,
                    model=device_info_domain.model
                )

                self.db.add(new_device)
                # Commit the transaction (this will automatically be handled by the context manager)
                return "created"
