class InfrastructureException(Exception):
    message = "Infrastructure Exception"
    status_code = 500

    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class DuplicateValueException(InfrastructureException):
    message = "Duplicate Value Exception"
    status_code = 409


class UniqueConstraintViolationException(InfrastructureException):
    def __init__(self, key: str, value: str):
        # Dynamically set the error message with the key and value
        self.key = key
        self.value = value
        self.message = f"Unique constraint violation: Key '{self.key}' with value '{self.value}' already exists."
        self.status_code = 409
        super().__init__(self.message)