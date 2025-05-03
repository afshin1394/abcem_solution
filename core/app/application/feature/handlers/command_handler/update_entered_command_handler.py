
from app.application.feature.commands.update_entered_at_walk_test_command import UpdateEnteredAtWalkTestCommand
from app.application.feature.queries.check_entered_at_walk_test_query import CheckEnteredAtWalkTestQuery
from app.application.feature.queries.validate_walk_test_time_duration_query import ValidateWalkTestTimeDurationQuery
from app.application.feature.shared.command_handler import CommandHandler
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.write.single.write_walk_test_repository import WriteWalkTestRepository


class UpdateEnteredAtWalkTestCommandHandler(CommandHandler[UpdateEnteredAtWalkTestCommand,None]):

    def __init__(self,write_walk_test_repository : WriteWalkTestRepository, cache_gateway: CacheGateway):
        super().__init__(cache_gateway)
        self.write_walk_test_repository = write_walk_test_repository
    async def handle(self, command: UpdateEnteredAtWalkTestCommand):
       await self.write_walk_test_repository.update_entered_at(command.walk_test_id)

    async def get_related_cache_keys(self, command: UpdateEnteredAtWalkTestCommand) -> list[str]:
        return [await CheckEnteredAtWalkTestQuery(walk_test_id=command.walk_test_id).generate_cache_key(),await ValidateWalkTestTimeDurationQuery(walk_test_id=command.walk_test_id).generate_cache_key()]