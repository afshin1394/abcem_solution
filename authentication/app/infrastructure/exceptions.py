#Redis
class InfrastructureException(Exception):

    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        self.message = message


class RedisSetException(InfrastructureException):
    def __init__(self,key : str):
        super().__init__(f"failed to set {key}  on redis.", error_code=500)


class RedisConnectionException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to connect to redis.", error_code=500)


class RedisGetException(InfrastructureException):
    def __init__(self ,key : str):
        super().__init__(f"failed to get {key} value from redis.", error_code=500)


#postgres
class DataBaseConnectionException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to connect to postgres.", error_code=500)

class DatabaseReadException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to read from postgres.", error_code=500)

class DatabaseWriteException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to write to postgres.", error_code=500)


#remote
class RemoteServicesException(InfrastructureException):
    def __init__(self):
        super().__init__("remote service not available.", error_code=500)


class SMSServicesException(InfrastructureException):
    def __init__(self):
        super().__init__("sms service not available.", error_code=500)
class FailedSendingSMSException(InfrastructureException):
    def __init__(self):
        super().__init__("failed to send the sms.", error_code=500)




