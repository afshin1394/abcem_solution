from datetime import datetime

from pydantic import BaseModel

class TokenDomain(BaseModel):
    access_token: str
    access_token_expiration_date: str
    refresh_token: str
    refresh_token_expiration_date: str