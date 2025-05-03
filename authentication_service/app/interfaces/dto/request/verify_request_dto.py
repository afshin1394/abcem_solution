from pydantic import BaseModel

class VerifyRequestDTO(BaseModel):
     otp:str
     session_id: str