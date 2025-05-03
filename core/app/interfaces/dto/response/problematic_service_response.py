from typing import List

from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse


class ProblematicService(BaseModel):
    id : int
    name : str

class ProblematicServiceResponse(BaseSuccessResponse[List[ProblematicService]]):
    pass
