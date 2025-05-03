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

class UpdateSpeedTestServersRequest(BaseModel):
    servers : list[SpeedTestServer]