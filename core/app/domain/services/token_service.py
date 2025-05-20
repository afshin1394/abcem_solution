from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    async def validate_access_token(self, access_token: str) -> bool:
        raise NotImplementedError()