from dataclasses import dataclass

@dataclass
class SpeedTestServerDomain:
    id: int
    name: str
    sponsor: str
    host: str
    country: str
    lat: float
    lon: float
    distance: float
    url: str

