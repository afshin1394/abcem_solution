from typing import Optional

from pydantic import BaseModel

class LoginDomain(BaseModel):
    session_id: str
    otp: Optional[str] = None
