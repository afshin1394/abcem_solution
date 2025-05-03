

# src/infrastructure/services/get_ip_info_repository_impl.py

from typing import Optional
import httpx
from fastapi import Depends

from app.infrastructure.di.async_client import get_client
from app.domain.entities.ip_info_domain import IPInfoDomain
from app.domain.services.get_ip_info_service import GetIpInfoService

class GetIpInfoServiceImpl(GetIpInfoService):
    def __init__(self, client: httpx.AsyncClient = Depends(get_client)):
        self.client = client

    async def get_ip_info(self) -> IPInfoDomain:
        try:
            response = await self.client.get("https://ipinfo.io/2.146.4.53/json")
            response.raise_for_status()
            data = response.json()

            ip_info = IPInfoDomain(
                ip=data.get("ip"),
                hostname=data.get("hostname"),
                city=data.get("city"),
                region=data.get("region"),
                country=data.get("country"),
                loc=data.get("loc"),
                org=data.get("org"),
                postal=data.get("postal"),
                timezone=data.get("timezone"),
                readme=data.get("readme"),
                state = data.get("state")
            )
            return ip_info
        except httpx.HTTPError as e:
            # Log the error or handle it as needed
            raise e
