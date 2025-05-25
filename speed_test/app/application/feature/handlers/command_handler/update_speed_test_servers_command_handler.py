
from app.application.feature.commands.update_speed_test_servers_command import UpdateSpeedTestServersCommand
from app.application.feature.shared.command_handler import CommandHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.write.single.write_speed_test_server_repository import WriteSpeedTestServerRepository


class UpdateSpeedTestServersCommandHandler(CommandHandler[UpdateSpeedTestServersCommand,None]):

    def __init__(self, write_speed_test_server_repository: WriteSpeedTestServerRepository, cache_gateway: CacheGateway):
        super().__init__(cache_gateway)
        self.write_speed_test_server_repository = write_speed_test_server_repository
    async def handle(self, command: UpdateSpeedTestServersCommand):
         return await self.write_speed_test_server_repository.update_all(command.servers)


    async def get_related_cache_keys(self, command: UpdateSpeedTestServersCommand) -> list[str]:
        pass