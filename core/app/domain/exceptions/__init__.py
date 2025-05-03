class DomainException(Exception):
    message = "Domain Exception"
    status_code = 500

    def __init__(self, message=None, status_code=None):
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        super().__init__(self.message)

class WalkTestTimeDurationExceeded(DomainException):
    message = "Walk Test Time Exceeded"
    status_code = 422

class WalkTestLocationInvalid(DomainException):
    message = "Walk Test Location Invalid"
    status_code = 422