from typing import Optional

from app.application.feature.commands.bulk_insert_sms_command import BulkInsertSmsCommand
from app.application.feature.queries.get_n_last_sms_query import GetNLastSmsRecordsQuery
from app.application.feature.shared.command_handler import CommandHandler, C, E
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repository.write.write_sms_repository import WriteSmsRepository


class BulkInsertSmsCommandHandler(CommandHandler[BulkInsertSmsCommand,str]):

    def __init__(self,write_sms_repository : WriteSmsRepository ,cache_gateway: CacheGateway):
        super().__init__(cache_gateway)
        self.write_sms_repository = write_sms_repository


    async def handle(self, command: BulkInsertSmsCommand) -> Optional[str]:
      print(f"command + {command}")
      print(f"command.sms_list + {command.sms_list}")
      return await self.write_sms_repository.insert_all(command.sms_list)



    async def get_related_cache_keys(self, command: BulkInsertSmsCommand) -> list[str]:
        return [await GetNLastSmsRecordsQuery().generate_cache_key()]
