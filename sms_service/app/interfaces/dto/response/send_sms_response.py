from pydantic import  model_validator

from app.interfaces.dto.success_response import BaseSuccessResponse


class SendSmsResponse(BaseSuccessResponse[str]):
    pass

    class Config:
        exclude_none = True

    @model_validator(mode='before')
    def remove_none_values(cls, values):
        # Remove fields with None values
        return {k: v for k, v in values.items() if v is not None}