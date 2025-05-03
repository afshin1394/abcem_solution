class ApplicationException(Exception):
    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        self.message = message
