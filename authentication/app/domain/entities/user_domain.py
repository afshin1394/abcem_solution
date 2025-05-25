from pydantic import BaseModel

class UserDomain(BaseModel):
    msisdn: str
