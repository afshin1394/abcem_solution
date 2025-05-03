from app.application.feature.commands.update_speed_test_servers_command import UpdateSpeedTestServersCommand
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain
from app.infrastructure.mapper.mapper import map_models



class UpdateSpeedTestServersUseCase(BaseUseCase):

    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    async def __execute__(self, **kwargs):
        update_speed_test_server_request = kwargs.get("update_speed_test_server_request")
        print("update_speed_test_server_request" + update_speed_test_server_request.__str__())
        servers = []
        for server in update_speed_test_server_request.servers:
           server_domain = await map_models(server,SpeedTestServerDomain)
           servers.append(server_domain)
        update_speed_test_server_command = UpdateSpeedTestServersCommand(servers= servers)
        return await self.mediator.send(update_speed_test_server_command)


