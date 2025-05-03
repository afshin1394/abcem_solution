from app.domain.entities.ip_info_domain import IPInfoDomain
from app.domain.services.get_ip_info_service import GetIpInfoService


class GetIpInfoServiceImpl:
        def __init__(self, service: GetIpInfoService):
                self.service = service

        async def execute(self) -> IPInfoDomain:
                ip_info_domain =  await self.service.get_ip_info()
                return ip_info_domain

