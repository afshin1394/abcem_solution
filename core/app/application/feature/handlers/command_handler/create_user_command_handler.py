from app.application.feature.commands.create_user_command import CreateUserCommand
from app.application.feature.shared.command_handler import CommandHandler, C
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.users_domain import UserDomain
from app.domain.events.user_created_event import UserCreatedEvent
from app.domain.repositories.users_repository import UsersRepository


class CreateUserCommandHandler(CommandHandler[CreateUserCommand, UserCreatedEvent]):
    async def get_related_cache_keys(self, command: C) -> list[str]:
        pass

    def __init__(self, user_repository: UsersRepository, cache_gateway: CacheGateway):
        super().__init__(cache_gateway)
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> UserCreatedEvent:
        return await self.user_repository.save(UserDomain(name=command.name, age=command.age, gender=command.gender))

