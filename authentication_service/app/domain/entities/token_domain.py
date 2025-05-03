from pydantic import BaseModel

class TokenDomain(BaseModel):
    access_token: str
    refresh_token: str