from app.application.feature.shared.command import Command


class CreateUserCommand(Command):
    name: str
    age: int
    gender: str
