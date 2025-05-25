from fastapi.params import Depends

from app.application.feature.commands.bulk_insert_sms_command import BulkInsertSmsCommand
from app.application.feature.commands.insert_sms_command import InsertSmsCommand
from app.application.feature.handlers.command_handler.bulk_insert_sms_command_handler import BulkInsertSmsCommandHandler
from app.application.feature.handlers.command_handler.insert_sms_command_handler import InsertSmsCommandHandler
from app.application.feature.handlers.query_handler.get_n_last_query_handler import GetNLastSMSRecordQueryHandler
from app.application.feature.queries.get_n_last_sms_query import GetNLastSmsRecordsQuery
from app.application.mediator import Mediator
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repository.read.read_sms_repository import ReadSmsRepository
from app.domain.repository.write.write_sms_repository import WriteSmsRepository
from app.infrastructure.di import get_cache
from app.infrastructure.di.repository import get_read_sms_repository, get_write_sms_repository


def get_mediator(
        cache_gateway: CacheGateway = Depends(get_cache),
        read_sms_repository : ReadSmsRepository = Depends(get_read_sms_repository),
        write_sms_repository : WriteSmsRepository = Depends(get_write_sms_repository),

) -> Mediator:
    mediator = Mediator()

    # queries
    mediator.register_handler(GetNLastSmsRecordsQuery,GetNLastSMSRecordQueryHandler(read_sms_repository=read_sms_repository,cache_gateway=cache_gateway,expire=3600))

    #commands
    mediator.register_handler(InsertSmsCommand,InsertSmsCommandHandler(write_sms_repository=write_sms_repository,cache_gateway=cache_gateway))
    mediator.register_handler(BulkInsertSmsCommand,BulkInsertSmsCommandHandler(write_sms_repository=write_sms_repository,cache_gateway=cache_gateway))

    return mediator
