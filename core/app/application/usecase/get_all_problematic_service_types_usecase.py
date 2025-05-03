from typing import Any, List

from app.application.feature.queries.get_all_problematic_service_type_query import GetAllProblematicServiceTypeQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.problematic_service_domain import ProblematicServiceDomain


class GetAllProblematicServiceTypesUseCase(BaseUseCase):

    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> List[ProblematicServiceDomain]:
        return await self.mediator.send(GetAllProblematicServiceTypeQuery())
