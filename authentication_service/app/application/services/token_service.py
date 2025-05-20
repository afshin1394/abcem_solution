from abc import ABC, abstractmethod

from app.domain.entities.token_domain import TokenDomain
from app.domain.entities.user_domain import UserDomain


class TokenService(ABC):
    @abstractmethod
    async def generate_tokens(self, session_id: str,otp_code : str,**kwargs) -> TokenDomain:
        raise NotImplementedError()

    @abstractmethod
    async def generate_tokens_based_on_refresh_token(self, refresh_token: str) -> TokenDomain:
        raise NotImplementedError

    @abstractmethod
    async def generate_session_id(self, user: UserDomain) -> str:
        raise NotImplementedError

    @abstractmethod
    async def validate_refresh_token(self, refresh_token: str) -> bool:
        raise NotImplementedError()
    @abstractmethod
    async def validate_access_token(self, access_token: str) -> bool:
        raise NotImplementedError()