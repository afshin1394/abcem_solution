from typing import List

from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse

class ComplaintType(BaseModel):
    id : int
    name : str


class ComplaintTypeResponse(BaseSuccessResponse[List[ComplaintType]]):
    pass