from app.application.feature.shared.command import Command
from app.domain.entities.sms_record_domain import SMSRecordDomain


class BulkInsertSmsCommand(Command):
    sms_list : list[SMSRecordDomain]