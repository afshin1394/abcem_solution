from abc import abstractmethod, ABC

from app.domain.entities.device_info_domain import DeviceInfoDomain


class WriteDeviceInfoRepository(ABC):
    @abstractmethod
    async def update_device_info(self,device_info_domain : DeviceInfoDomain):
        pass