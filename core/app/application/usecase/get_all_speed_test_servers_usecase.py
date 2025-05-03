
from app.application.feature.queries.get_all_speed_test_servers_query import GetAllSpeedTestServersQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain


class GetAllSpeedTestServersUseCase(BaseUseCase):

    def __init__(self,mediator : Mediator):
        super().__init__()
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> list[SpeedTestServerDomain]:
         return await self.mediator.send(GetAllSpeedTestServersQuery())
