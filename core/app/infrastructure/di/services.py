import httpx
from fastapi import Depends

from app.domain.services.get_ip_info_service import GetIpInfoService
from app.domain.services.gis_service import GISService
from app.infrastructure.di.async_client import get_client
from app.infrastructure.repository_impl.get_ip_info_repository_impl import GetIpInfoServiceImpl
from app.infrastructure.services_impl.are_all_locations_within_distance_service_impl import GISServiceImpl


#services
async def get_ip_info_service(client: httpx.AsyncClient = Depends(get_client)) -> GetIpInfoService:
    return GetIpInfoServiceImpl(client=client)


async def get_gis_service() -> GISService:
    return GISServiceImpl()