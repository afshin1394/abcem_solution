from abc import ABC, abstractmethod

from app.domain.entities.sms_record_domain import SMSRecordDomain


class WriteSmsRepository(ABC):

    @abstractmethod
    async def insert(self, sms_record_domain: SMSRecordDomain):
        raise NotImplementedError()
    @abstractmethod
    async def insert_all(self,sms_record_domain_list: list[SMSRecordDomain]):
        raise NotImplementedError()
