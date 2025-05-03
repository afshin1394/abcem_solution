from typing import  List

from app.application.feature.queries.get_all_technology_types_query import GetAllTechnologyTypesQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.technology_type_domain import TechnologyTypeDomain


class GetAllTechnologyTypesUseCase(BaseUseCase):
    def __init__(self, mediator: Mediator) -> None:
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> List[TechnologyTypeDomain]:
        return await self.mediator.send(GetAllTechnologyTypesQuery())
