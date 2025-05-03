
from abc import ABC, abstractmethod

from app.domain.entities.ip_info_domain import IPInfoDomain


class GetIpInfoService:
    @abstractmethod
    async def get_ip_info(self) -> IPInfoDomain:
        pass

