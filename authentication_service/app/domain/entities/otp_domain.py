from pydantic import BaseModel

class LoginDomain(BaseModel):
    session_id: str
    otp: str
