from typing import List

from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse


class TechnologyType(BaseModel):
    id: int
    name: str


class TechnologyTypeResponse(BaseSuccessResponse[List[TechnologyType]]):
    pass
