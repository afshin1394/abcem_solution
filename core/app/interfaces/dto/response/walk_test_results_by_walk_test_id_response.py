from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel

from app.domain.enums.step_test_type_enum import StepTestTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.interfaces.dto.success_response import BaseSuccessResponse
class DeviceInfoByWalkTestId(BaseModel):
    security_patch: datetime
    sdk: int
    os_version: int
    brand: str
    device: str
    hardware: str
    model: str
    walk_test_id: str

class WalkTestResultsByWalkTestId(BaseModel):
    step_number: int
    step_type_id: StepTestTypeEnum
    walk_test_id: str
    walk_test_detail_id: str

    call_test_id: Optional[str] = None
    drop_call: Optional[int] = None
    technology_id: Optional[TechnologyEnum] = None
    is_voltE: Optional[bool] = None

    cell_info_id: Optional[str] = None
    cell_data: Optional[Dict[str, Any]] = None
    level: Optional[float] = None
    quality: Optional[float] = None

    speed_test_result_id: Optional[str] = None
    download: Optional[float] = None
    upload: Optional[float] = None
    ping: Optional[float] = None
    jitter: Optional[float] = None
    speed_test_result_technology_id: Optional[TechnologyEnum] = None

    class Config:
        exclude_none = True  # This ensures None fields are dropped when .dict() or .json() is used


class WalkTestResultsWithDeviceInfoComposition(BaseModel):
     device_info : DeviceInfoByWalkTestId
     steps : List[WalkTestResultsByWalkTestId]


class WalkTestResultsByWalkTestIdResponse(BaseSuccessResponse[WalkTestResultsWithDeviceInfoComposition]):
    pass


    class Config:
        exclude_none = True