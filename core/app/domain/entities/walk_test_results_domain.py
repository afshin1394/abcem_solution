from dataclasses import dataclass
from typing import Optional, Any, Dict

from app.domain.enums.step_test_type_enum import StepTestTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum

@dataclass
class WalkTestResultsDomain:
    step_number: int
    step_type_id: StepTestTypeEnum
    walk_test_id: str
    walk_test_detail_id: str

    call_test_id: Optional[str]
    drop_call: Optional[int]
    technology_id: Optional[TechnologyEnum]
    is_voltE: Optional[bool]

    cell_info_id: str
    cell_data: Optional[Dict[str, Any]]
    level: Optional[float]
    quality: Optional[float]

    speed_test_result_id: Optional[str]
    download: Optional[float]
    upload: Optional[float]
    ping: Optional[float]
    jitter: Optional[float]
    speed_test_result_technology_id: Optional[TechnologyEnum]

