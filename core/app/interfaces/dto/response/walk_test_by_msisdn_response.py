from datetime import time
from typing import List, Optional

from pydantic import BaseModel, Field

from app.domain.enums.complaint_type_enum import ComplaintTypeEnum
from app.domain.enums.problematic_service_enum import ProblematicServiceEnum
from app.domain.enums.service_type_enum import ServiceTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.interfaces.dto.success_response import BaseSuccessResponse


class WalkTestByMSISDN(BaseModel):
    id : str
    province: str
    region: str
    city: str
    is_village: bool
    latitude: float
    longitude: float
    serving_cell: str
    serving_site: str
    msisdn: str
    is_at_all_hours : bool
    start_time_of_issue: Optional[time] = None
    end_time_of_issue: Optional[time] = None
    technology_type_id: TechnologyEnum
    complaint_type_id: ComplaintTypeEnum
    problematic_service_id: ProblematicServiceEnum
    service_type_id: ServiceTypeEnum


class WalkTestByMSISDNResponse(BaseSuccessResponse[List[WalkTestByMSISDN]]):
    pass
