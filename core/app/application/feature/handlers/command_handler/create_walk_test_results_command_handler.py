
from app.application.feature.commands.create_walk_test_command import CreateWalkTestCommand
from app.application.feature.commands.create_walk_test_results_command import CreateWalkTestResultsCommand
from app.application.feature.shared.command_handler import CommandHandler, C
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.write.multi.write_walk_test_result_unit_of_work import WriteWalkTestResultUnitOfWork


class CreateWalkTestResultsCommandHandler(CommandHandler[CreateWalkTestCommand, str]):

    async def get_related_cache_keys(self, command: C) -> list[str]:
        pass

    def __init__(self, cache_gateway: CacheGateway, write_walk_test_result_unit_of_work: WriteWalkTestResultUnitOfWork):
        super().__init__(cache_gateway)
        self.write_walk_test_result_unit_of_work = write_walk_test_result_unit_of_work

    async def handle(self, create_walk_test_results_command: CreateWalkTestResultsCommand
                     ):
        result = await self.write_walk_test_result_unit_of_work.transact(
            walk_test_id= create_walk_test_results_command.walk_test_id,
            call_test_domain= create_walk_test_results_command.call_test_list,
            cell_info_result_domain= create_walk_test_results_command.cell_info_list,
            speed_test_result_domain= create_walk_test_results_command.speed_test_list,
            walk_test_detail_domain= create_walk_test_results_command.walk_test_detail_list
        )
        return result
