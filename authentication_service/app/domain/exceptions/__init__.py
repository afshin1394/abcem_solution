class DomainException(Exception):
    message = "Domain Exception"
    status_code = 500  # Internal Server Error (default)

    def __init__(self, message=None, status_code=None):
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        super().__init__(self.message)


class InvalidOTPException(DomainException):
    message = "Invalid or expired OTP"
    status_code = 400  # Bad Request (OTP errors are client-related)


class InvalidSessionException(DomainException):
    message = "Invalid or expired session ID"
    status_code = 401  # Unauthorized (session expiration is auth-related)


class UserCreationException(DomainException):
    message = "User cannot be created"
    status_code = 409  # Conflict (user creation failure due to duplication or constraints)


class RefreshTokenExpiredException(DomainException):
    message = "Refresh token expired or invalid"
    status_code = 401  # Unauthorized (since token expiration affects authentication)


class FailAddingToBlacklistException(DomainException):
    message = "failed adding to blacklist"
    status_code = 500  # Internal Server Error (since it's a system failure)