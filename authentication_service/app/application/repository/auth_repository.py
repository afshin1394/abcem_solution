from abc import ABC, abstractmethod

from app.domain.entities.otp_domain import LoginDomain


class AuthRepository(ABC):
    @abstractmethod
    async def save_otp(self, otp: str):
        pass

    @abstractmethod
    async def get_otp(self, msisdn: str) -> LoginDomain:
        pass

    @abstractmethod
    async def save_session_id(self, session_id: str):
        pass

    @abstractmethod
    async def get_session_id(self,session_id : str) -> str:
        pass

