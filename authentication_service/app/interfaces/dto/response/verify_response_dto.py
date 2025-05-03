

from app.domain.entities.token_domain import TokenDomain
from app.interfaces.dto.response.base_response import BaseResponse
from pydantic import BaseModel

class VerifyResult(BaseModel):
     access_token: str
     refresh_token: str


class VerifyResponseDTO(BaseResponse[VerifyResult]):
     @classmethod
     def from_domain(cls,token_domain : TokenDomain) -> 'VerifyResponseDTO' :
         return cls(
               result= VerifyResult(
                    access_token=token_domain.access_token,
                    refresh_token=token_domain.refresh_token
               )
          )