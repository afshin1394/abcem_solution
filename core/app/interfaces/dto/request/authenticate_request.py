from pydantic import BaseModel, Field, field_validator

class AuthenticateRequest(BaseModel):
    msisdn: str = Field(..., description="The user's mobile phone number")

    @field_validator("msisdn")
    def validate_msisdn(cls, value: str) -> str:
        import re
        pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
        if not pattern.match(value):
            raise ValueError("Invalid MSISDN format. It must follow the E.164 standard.")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "msisdn": "+12345678901"
            }
        }
