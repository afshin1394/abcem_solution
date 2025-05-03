from typing import Optional

from app.application.feature.commands.update_walk_test_status_command import UpdateWalkTestStatusCommand
from app.application.feature.shared.command_handler import CommandHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.write.single.write_walk_test_repository import WriteWalkTestRepository


class UpdateWalkTestStatusCommandHandler(CommandHandler[UpdateWalkTestStatusCommand, None]):


     def __init__(self,write_walk_test_repository : WriteWalkTestRepository, cache_gateway: CacheGateway):
         super().__init__(cache_gateway)
         self.write_walk_test_repository = write_walk_test_repository

     async def get_related_cache_keys(self, command: UpdateWalkTestStatusCommand) -> list[str]:
        pass


     async def handle(self, command: UpdateWalkTestStatusCommand) :
       await self.write_walk_test_repository.update_walk_test_status(walk_test_id=command.walk_test_id,walk_test_status=command.walk_test_status)
