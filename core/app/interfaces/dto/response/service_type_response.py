from typing import List

from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse


class ServiceType(BaseModel):
    id: int
    name: str


class ServiceTypeResponse(BaseSuccessResponse[List[ServiceType]]):
    pass
