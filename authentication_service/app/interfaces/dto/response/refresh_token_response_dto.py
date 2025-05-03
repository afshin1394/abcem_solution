
from app.interfaces.dto.response.base_response import BaseResponse


class RefreshTokenResponseDTO(BaseResponse[str]):

     @classmethod
     def from_domain(cls, access_token: str) :
          cls(
              result=access_token
          )
