from typing import Optional

from app.domain.entities.otp_domain import LoginDomain
from app.interfaces.dto.response.base_response import BaseResponse
from pydantic import BaseModel

class LoginResult(BaseModel):
    session_id: str
    otp:Optional[str] = None

class LoginResponseDTO(BaseResponse[LoginResult]):

    @classmethod
    def from_domain(cls, otp_domain: LoginDomain):
        return cls(
            result= LoginResult(
               session_id= otp_domain.session_id,
               otp= otp_domain.otp
            ),
        )
