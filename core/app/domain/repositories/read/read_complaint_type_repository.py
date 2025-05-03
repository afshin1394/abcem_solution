from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.complaint_type_domain import ComplaintTypeDomain


class ReadComplaintTypeRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[ComplaintTypeDomain]:
        pass