class InterfaceException(Exception):
    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        super().__init__(message)

class InvalidSessionIdException(InterfaceException):
    def __init__(self, key: str):
        super().__init__(f"session {key} is invalid ", error_code=10001)

class InvalidOtpException(InterfaceException):
    def __init__(self, key: str):
        super().__init__(f"session {key} is invalid ", error_code=10002)


class InvalidTokenException(InterfaceException):
    def __init__(self, key: str):
        super().__init__(f"token {key} is invalid ", error_code=10003)


class MSISDNLengthException(InterfaceException):
    def __init__(self):
        super().__init__(f"phone length is invalid", error_code=10003)

class MSISDNFormatException(InterfaceException):
    def __init__(self):
        super().__init__(f"phone format is invalid", error_code=10003)