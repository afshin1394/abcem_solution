

from app.application.feature.commands.create_walk_test_command import CreateWalkTestCommand
from app.application.feature.queries.get_walk_test_by_msisdn_query import GetWalkTestByMSISDNQuery
from app.application.feature.shared.command_handler import CommandHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.walk_test_domain import WalkTestDomain
from app.domain.repositories.write.single.write_walk_test_repository import WriteWalkTestRepository
from app.infrastructure.mapper.mapper import map_models


class CreateWalkTestCommandHandler(CommandHandler[CreateWalkTestCommand,None]):

    def __init__(self, write_walk_test_repository: WriteWalkTestRepository, cache_gateway: CacheGateway):
        super().__init__(cache_gateway)
        self.write_walk_test_repository = write_walk_test_repository

    async def handle(self, command: CreateWalkTestCommand):

        walk_test_domain = await map_models(command, WalkTestDomain)
        print("walk_test_domain" + str(walk_test_domain))
        await self.write_walk_test_repository.create_walk_test(walk_test_domain)


    async def get_related_cache_keys(self, command: CreateWalkTestCommand) -> list[str]:
        return [await GetWalkTestByMSISDNQuery(msisdn=command.msisdn).generate_cache_key()]
