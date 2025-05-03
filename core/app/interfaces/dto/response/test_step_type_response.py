from typing import List
from pydantic import BaseModel
from app.interfaces.dto.success_response import BaseSuccessResponse


class TestStepType(BaseModel):
     id : int
     name : str



class TestStepTypeResponse(BaseSuccessResponse[List[TestStepType]]):
       pass