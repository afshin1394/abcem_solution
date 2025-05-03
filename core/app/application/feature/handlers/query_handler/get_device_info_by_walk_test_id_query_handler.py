from app.application.feature.queries.get_device_info_by_walk_test_id_query import GetDeviceInfoByWalkTestIdQuery
from app.application.feature.shared.query_handler import QueryHandler, Q, R
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.device_info_domain import DeviceInfoDomain
from app.domain.repositories.read.read_device_info_repository import ReadDeviceInfoRepository


class GetDeviceInfoByWalkTestIdQueryHandler(QueryHandler[GetDeviceInfoByWalkTestIdQuery,DeviceInfoDomain]):


    def __init__(self,read_device_info_repository : ReadDeviceInfoRepository, cache_gateway: CacheGateway, cache_enabled: bool = True, expire: int = 1800):
        super().__init__(cache_gateway, cache_enabled, expire)
        self.read_device_info_repository = read_device_info_repository

    async def handle(self, query: GetDeviceInfoByWalkTestIdQuery) -> DeviceInfoDomain:
      return  await self.read_device_info_repository.get_device_info_by_walk_test_id(query.walk_test_id)
