from abc import ABC, abstractmethod

from app.domain.entities.device_info_domain import DeviceInfoDomain


class ReadDeviceInfoRepository(ABC):

     @abstractmethod
     async def get_device_info_by_walk_test_id(self,walk_test_id : str) -> DeviceInfoDomain:
         raise NotImplementedError