from abc import ABC, abstractmethod

from app.domain.entities import PaginatedResult
from app.domain.entities.sms_record_domain import SMSRecordDomain


class ReadSmsRepository(ABC):

     @abstractmethod
     async def get_n_last_sms(self,page : int,page_size : int) -> PaginatedResult[SMSRecordDomain]:
        raise NotImplementedError