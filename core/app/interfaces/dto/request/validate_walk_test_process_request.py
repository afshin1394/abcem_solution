from pydantic import BaseModel


class ValidateWalkTestProcessRequest(BaseModel):
    walk_test_id: str
    gps_lat : float
    gps_lon : float
    map_lat : float
    map_lon : float