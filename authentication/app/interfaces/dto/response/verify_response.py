
from app.domain.entities.token_domain import TokenDomain
from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse


class VerifyResult(BaseModel):
     access_token: str
     access_token_expires_at: str
     refresh_token: str
     refresh_token_expires_at: str


class VerifyResponse(BaseSuccessResponse[VerifyResult]):
     @classmethod
     def from_domain(cls,token_domain : TokenDomain) -> 'VerifyResponse':
         return cls(
               result= VerifyResult(
                    access_token=token_domain.access_token,
                    access_token_expires_at=token_domain.access_token_expiration_date,
                    refresh_token=token_domain.refresh_token,
                    refresh_token_expires_at=token_domain.refresh_token_expiration_date
               )
          )