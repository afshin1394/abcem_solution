from typing import List

from app.application.feature.queries.get_all_test_step_type_query import GetAllTestStepTypeQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.step_test_type_domain import StepTestTypeDomain


class GetAllTestStepTypeUseCase(BaseUseCase):


    def __init__(self,mediator : Mediator):
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> List[StepTestTypeDomain]:
       return await self.mediator.send(GetAllTestStepTypeQuery())
