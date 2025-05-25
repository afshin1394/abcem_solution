
from app.application.feature.commands.insert_sms_command import InsertSmsCommand
from app.application.feature.queries.get_n_last_sms_query import GetNLastSmsRecordsQuery
from app.application.feature.shared.command_handler import CommandHandler, C, E
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.sms_record_domain import SMSRecordDomain
from app.domain.enums.sms_status_enum import SmsStatusEnum
from app.domain.repository.write.write_sms_repository import WriteSmsRepository


class InsertSmsCommandHandler(CommandHandler[InsertSmsCommand,str]):

    def __init__(self,write_sms_repository : WriteSmsRepository, cache_gateway: CacheGateway):
        super().__init__(cache_gateway)
        self.write_sms_repository = write_sms_repository

    async def handle(self, command: InsertSmsCommand):
        print(f"command + {command}",flush=True)
        await self.write_sms_repository.insert(SMSRecordDomain(phone_number=command.phone_number,message=command.message,status=SmsStatusEnum.SENT,sms_id=command.correlation_id))


    async def get_related_cache_keys(self, command: InsertSmsCommand) -> list[str]:
        return [await GetNLastSmsRecordsQuery().generate_cache_key()]