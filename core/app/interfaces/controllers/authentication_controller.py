from app.application.feature.commands.authenticate_command import AuthenticateCommand
from app.application.mediator import Mediator
from app.domain.events.authenticated_event import AuthenticatedEvent
from app.interfaces.dto.request.authenticate_request import AuthenticateRequest


class AuthenticationController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    async def authenticate(self, authenticate_request: AuthenticateRequest) -> str:
        authenticate_cmd = AuthenticateCommand(msisdn=authenticate_request.msisdn)
        response = await  self.mediator.send(authenticate_cmd)
        if isinstance(response, AuthenticatedEvent):
            return "response"
        else:
            raise ValueError("Invalid response type from handler.")
