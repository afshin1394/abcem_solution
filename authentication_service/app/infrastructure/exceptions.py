#Redis
class InfrastructureException(Exception):

    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        self.message = message


class RedisSetException(InfrastructureException):
    def __init__(self,key : str):
        super().__init__(f"failed to set {key}  on redis.", error_code=1001)


class RedisConnectionException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to connect to redis.", error_code=1002)


class RedisGetException(InfrastructureException):
    def __init__(self ,key : str):
        super().__init__(f"failed to get {key} value from redis.", error_code=1003)


#postgres
class DataBaseConnectionException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to connect to postgres.", error_code=2001)

class DatabaseReadException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to read from postgres.", error_code=2002)

class DatabaseWriteException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to write to postgres.", error_code=2003)


#remote
class RemoteServicesException(InfrastructureException):
    def __init__(self):
        super().__init__("remote service not available.", error_code=3001)


class SMSServicesException(InfrastructureException):
    def __init__(self):
        super().__init__("sms service not available.", error_code=3002)
