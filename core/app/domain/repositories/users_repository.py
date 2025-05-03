
from abc import  abstractmethod
from typing import List

from app.domain.entities.users_domain import UserDomain
from app.domain.events.user_created_event import UserCreatedEvent


class UsersRepository:
    @abstractmethod
    async def save(self, userDomain: UserDomain) -> UserCreatedEvent:
        pass

    @abstractmethod
    async def get_all(self) -> List[UserDomain]:
        pass

