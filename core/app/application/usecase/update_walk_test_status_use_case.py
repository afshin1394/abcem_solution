
from app.application.feature.commands.update_walk_test_status_command import UpdateWalkTestStatusCommand
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.infrastructure.mapper.mapper import map_models
from app.interfaces.dto.request.update_walk_test_status_request import UpdateWalkTestStatusRequest


class UpdateWalkTestStatusUseCase(BaseUseCase):


    def __init__(self,mediator : Mediator):
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> None:
        update_walk_test_status_request = kwargs.get("update_walk_test_status_request")
        if isinstance(update_walk_test_status_request, UpdateWalkTestStatusRequest):
            print("update_walk_test_status_request" + update_walk_test_status_request.__str__())
            update_walk_test_status_command = await map_models(update_walk_test_status_request, UpdateWalkTestStatusCommand)
            return await self.mediator.send(update_walk_test_status_command)
        else:
            print("The argument is not of type 'update_walk_test_status_request'")
