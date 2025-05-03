
from app.domain.enums.complaint_type_enum import ComplaintTypeEnum
from app.domain.enums.problematic_service_enum import ProblematicServiceEnum
from app.domain.enums.service_type_enum import ServiceTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum
from pydantic import BaseModel, Field, model_validator, field_validator, validator
from typing import Optional
from datetime import time


class WalkTestRequest(BaseModel):
    ref_id: str = Field(default=None, description="Reference ID for the walk test.")
    province: str = Field(default=None, description="Province where the walk test is conducted.")
    region: str = Field(default=None, description="Region where the walk test is conducted.")
    city: str = Field(default=None, description="City where the walk test is conducted.")
    is_village: bool = Field(default=None, description="Indicates if the location is a village.")
    latitude: float = Field(default=35.788161, description="Latitude of the location.", le=90, ge=-90)
    longitude: float = Field(default=51.505264, description="Longitude of the location.", le=180, ge=-180)
    serving_cell: Optional[str] = Field(default=None, description="Serving cell information.")
    serving_site: Optional[str] = Field(default=None, description="Serving site information.")
    is_at_all_hours: bool = Field(default=None, description="Indicates if the problem is at all hours")
    start_time_of_issue: Optional[time] = Field(default=None, description="Start time of issue.")
    end_time_of_issue: Optional[time] = Field(default=None, description="End time of issue.",)
    msisdn: str = Field(default=None, description="MSISDN (phone number) associated with the test.")
    contact_number: str = Field(default=None, description="Contact number.")
    technology_type_id: TechnologyEnum = Field(default=None, description="Technology used in the test.")
    complaint_type_id: ComplaintTypeEnum = Field(default=None, description="Type of complaint.")
    problematic_service_id: ProblematicServiceEnum = Field(default=None, description="Problematic service.")
    service_type_id: ServiceTypeEnum = Field(default=None, description="Service type.(FDD = 1 or TDD = 2)")
    related_tt: str = Field(default=None, description="Related trouble ticket.")
    walk_test_status_id: WalkTestStatusEnum = Field(default=None, description="Status of the walk test.")


    @field_validator('start_time_of_issue', 'end_time_of_issue', mode='before',check_fields=True)
    def allow_none(cls, v):
        if v is None:
            return None
        return v



    @model_validator(mode='after')
    def check_time_range_aval(cls, model: 'WalkTestRequest') -> 'WalkTestRequest':
        if model.is_at_all_hours is False:
            if model.start_time_of_issue is None or model.end_time_of_issue is None:
                raise ValueError("you must provide start_time_of_issue, end_time_of_issue.")
            if model.start_time_of_issue >= model.end_time_of_issue:
                raise ValueError("start_time_of_issue must be before end_time_of_issue.")
        else:
            if model.start_time_of_issue is not None or model.end_time_of_issue is not None:
                raise ValueError("you must not provide start_time_of_issue, end_time_of_issue because is_at_all_hours is True.")


        return model

    class Config:
        populate_by_name = True
        from_attribute = True
        arbitrary_types_allowed = True
