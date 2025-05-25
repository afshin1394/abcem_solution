
from app.domain.entities.otp_domain import LoginDomain
from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse


class LoginResult(BaseModel):
    session_id: str

class LoginResponse(BaseSuccessResponse[LoginResult]):

    @classmethod
    def from_domain(cls, otp_domain: LoginDomain):
        return cls(
            result= LoginResult(
               session_id= otp_domain.session_id,
            ),
        )
