from typing import List

from app.interfaces.dto.success_response import BaseSuccessResponse
from pydantic import BaseModel



class SpeedTestServer(BaseModel):
    id: int
    name: str
    sponsor: str
    host: str
    country: str
    lat: float
    lon: float
    distance: float
    url: str





class SpeedTestsServersResponse(BaseSuccessResponse[List[SpeedTestServer]]):
    pass