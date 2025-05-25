from fastapi import Depends

from app.application.feature.commands.update_speed_test_servers_command import UpdateSpeedTestServersCommand
from app.application.feature.handlers.command_handler.update_speed_test_servers_command_handler import \
    UpdateSpeedTestServersCommandHandler
from app.application.mediator import Mediator
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.write_speed_test_server_repository import WriteSpeedTestServerRepository
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.repositories import get_write_speed_test_server_repository


def get_mediator(
        cache_gateway: CacheGateway = Depends(get_cache),
        write_speed_test_server_repository: WriteSpeedTestServerRepository = Depends(get_write_speed_test_server_repository)

) -> Mediator:
    # commands
    mediator = Mediator()
    mediator.register_handler(UpdateSpeedTestServersCommand,
                              UpdateSpeedTestServersCommandHandler(write_speed_test_server_repository=write_speed_test_server_repository, cache_gateway=cache_gateway))



    return mediator
