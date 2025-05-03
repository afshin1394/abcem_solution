from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.step_test_type_domain import StepTestTypeDomain


class ReadTestStepTypeRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[StepTestTypeDomain]:
        pass