from typing import  List

from app.application.feature.queries.get_all_complaint_type_query import GetAllComplaintTypeQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.complaint_type_domain import ComplaintTypeDomain


class GetAllComplaintTypesUseCase(BaseUseCase):


        def __init__(self,mediator : Mediator):
            self.mediator = mediator

        async def __execute__(self, **kwargs) -> List[ComplaintTypeDomain]:
             return await self.mediator.send(GetAllComplaintTypeQuery())