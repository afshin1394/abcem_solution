from dataclasses import dataclass
from datetime import time
from typing import Optional

from app.domain.enums.complaint_type_enum import ComplaintTypeEnum
from app.domain.enums.problematic_service_enum import ProblematicServiceEnum
from app.domain.enums.service_type_enum import ServiceTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum


@dataclass
class WalkTestDomain:
    ref_id: str
    province: str
    region: str
    city: str
    is_village: bool
    latitude: float
    longitude: float
    serving_cell: str
    serving_site: str
    is_at_all_hours : bool
    start_time_of_issue: Optional[time]
    end_time_of_issue: Optional[time]
    msisdn: str
    technology_type_id: TechnologyEnum
    complaint_type_id: ComplaintTypeEnum
    problematic_service_id: ProblematicServiceEnum
    service_type_id: ServiceTypeEnum
    related_tt: str
    walk_test_status_id: WalkTestStatusEnum
    id : Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"WalkTestDomain(walk_test_id={self.id},ref_id={self.ref_id}, province={self.province}, region={self.region}, "
            f"city={self.city}, is_village={self.is_village}, latitude={self.latitude}, longitude={self.longitude}, "
            f"serving_cell={self.serving_cell}, serving_site={self.serving_site}, "
            f"start_time_of_issue={self.start_time_of_issue}, end_time_of_issue={self.end_time_of_issue}, "
            f"msisdn={self.msisdn}, technology={self.technology_type_id.name}, "
            f"complaint_type={self.complaint_type_id.name}, problematic_service={self.problematic_service_id.name}, "
            f"service_type_id={self.service_type_id.name}, related_tt={self.related_tt}, "
            f"walk_test_status_id={self.walk_test_status_id.name})"
        )

    def to_dict(self) -> dict:
        return {
            "ref_id": self.ref_id,
            "province": self.province,
            "region": self.region,
            "city": self.city,
            "is_village": self.is_village,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "serving_cell": self.serving_cell,
            "serving_site": self.serving_site,
            "is_at_all_hours": self.is_at_all_hours,
            "start_time_of_issue": self.start_time_of_issue.isoformat() if self.start_time_of_issue else None,
            "end_time_of_issue": self.end_time_of_issue.isoformat() if self.end_time_of_issue else None,
            "msisdn": self.msisdn,
            "technology_type_id": self.technology_type_id.name,
            "complaint_type_id": self.complaint_type_id.name,
            "problematic_service_id": self.problematic_service_id.name,
            "service_type_id": self.service_type_id.name,
            "related_tt": self.related_tt,
            "walk_test_status_id": self.walk_test_status_id.name,
        }