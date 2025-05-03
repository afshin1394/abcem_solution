from typing import Any

from app.application.feature.commands.create_user_command import CreateUserCommand
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.interfaces.dto.request.user_create_request import CreateUserRequest
from fastapi import logger


class CreateUserUseCase(BaseUseCase):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    async def __execute__(self, **kwargs) -> Any:
        create_user_request = kwargs.get("create_user_request")
        logger.logger.debug(msg=f'create_user {kwargs.keys().__str__()}')
        logger.logger.debug(msg=f'create_user {kwargs.values().__str__()}')
        if isinstance(create_user_request, CreateUserRequest):
            name = create_user_request.name
            age = create_user_request.age
            gender = create_user_request.gender

            print(f"Creating user: Name: {name}, Age: {age}, Gender: {gender}")

            # Safely convert age to int, and handle possible conversion errors
            try:
                age_int = int(age)  # Attempt to convert the age to an integer
            except ValueError:
                print(f"Invalid age value: {age}. Cannot convert to integer.")
                age_int = 0  # Default age value or handle error appropriately

            # Return a new CreateUserCommand object with the data
            await self.mediator.send(CreateUserCommand(name=name, age=age_int, gender=gender))
        else:
            print("The argument is not of type 'UserCreateRequest'")
