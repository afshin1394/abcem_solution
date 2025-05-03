from pydantic import BaseModel, Field

from app.interfaces.dto.success_response import BaseSuccessResponse


class Authentication(BaseModel):
    jwt_token: str = Field(..., description="The JWT token for authenticated requests")
    refresh_token: str = Field(..., description="The token used to refresh the JWT")

    class Config:
        json_schema_extra = {
            "example": {
                "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "def502009c4eb17..."
            }
        }


class AuthenticateResponse(BaseSuccessResponse[Authentication]):
    pass
