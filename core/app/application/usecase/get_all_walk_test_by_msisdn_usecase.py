from typing import Any, List

from app.application.feature.queries.get_walk_test_by_msisdn_query import GetWalkTestByMSISDNQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.entities.walk_test_domain import WalkTestDomain
from app.infrastructure.mapper.mapper import map_models
from app.interfaces.dto.request.get_walk_test_by_msisdn_request import GetWalkTestByMSISDNRequest


class GetAllWalkTestByMSISDNUseCase(BaseUseCase):

    def __init__(self, mediator: Mediator) -> None:
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> List[WalkTestDomain]:
        get_walk_test_by_msisdn_request = kwargs.get("get_walk_test_by_msisdn_request")
        if isinstance(get_walk_test_by_msisdn_request, GetWalkTestByMSISDNRequest):
            print("get_walk_test_by_msisdn_request" + get_walk_test_by_msisdn_request.__str__())
            walk_test_by_msisdn_query = await map_models(get_walk_test_by_msisdn_request, GetWalkTestByMSISDNQuery)
            return await self.mediator.send(walk_test_by_msisdn_query)
        else:
            print("The argument is not of type 'get_walk_test_by_msisdn_request'")


