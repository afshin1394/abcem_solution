from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse

class RefreshToken(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenResponse(BaseSuccessResponse[RefreshToken]):

    @classmethod
    def from_domain(cls, access_token: str, refresh_token: str):
        return cls(
            result=RefreshToken(access_token=access_token, refresh_token=refresh_token)
        )