from datetime import time
from typing import Optional

from app.application.feature.shared.command import Command
from app.domain.enums.complaint_type_enum import ComplaintTypeEnum
from app.domain.enums.problematic_service_enum import ProblematicServiceEnum
from app.domain.enums.service_type_enum import ServiceTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum


class CreateWalkTestCommand(Command):
    ref_id: str
    province: str
    region: str
    city: str
    is_village: bool
    latitude: float
    longitude: float
    serving_cell: str
    serving_site: str
    is_at_all_hours: bool
    start_time_of_issue: Optional[time]
    end_time_of_issue: Optional[time]
    msisdn: str
    technology_type_id: TechnologyEnum
    complaint_type_id: ComplaintTypeEnum
    problematic_service_id: ProblematicServiceEnum
    service_type_id: ServiceTypeEnum
    related_tt: str
    walk_test_status_id: WalkTestStatusEnum
