from datetime import time, datetime
from typing import Optional

import pytz
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, TIMESTAMP, Boolean, Float, ForeignKey, Integer, Time, DateTime
from sqlalchemy.sql import func
from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK
from .table_device_info import TableDeviceInfo
from .table_walk_test_detail import TableWalkTestDetail
from .table_technology_type import TableTechnologyType
from .table_complaint_type import TableComplaintType
from .table_problematic_service import TableProblematicService
from .table_service_type import TableServiceType
from .table_problematic_service import TableProblematicService
from .table_walk_test_status import TableWalkTestStatus



class TableWalkTest(BaseDBModelWithUUIDPK):
    __tablename__ = 'table_walk_test'
    ref_id = Column(String, unique=True)
    province = Column(String, nullable=True)
    region = Column(String, nullable=True)
    city = Column(String, nullable=True)
    is_village = Column(Boolean, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    serving_cell = Column(String, nullable=True)
    serving_site = Column(String, nullable=True)
    is_at_all_hours = Column(Boolean, nullable=True)
    start_time_of_issue: Optional[time] = Column(Time, nullable=True)
    end_time_of_issue: Optional[time] = Column(Time, nullable=True)
    times_of_day = Column(String, nullable=True)
    msisdn = Column(String, nullable=True)
    related_tt = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tehran')))
    entered_at = Column(DateTime(timezone=True), default=None ,nullable=True)

    technology_type_id = Column(Integer, ForeignKey('table_technology_type.id'), nullable=False)
    complaint_type_id = Column(Integer, ForeignKey('table_complaint_type.id'), nullable=False)
    problematic_service_id = Column(Integer, ForeignKey('table_problematic_service.id'), nullable=False)
    service_type_id = Column(Integer, ForeignKey('table_service_type.id'), nullable=False)
    walk_test_status_id = Column(Integer, ForeignKey('table_walk_test_status.id'), nullable=False)


    walk_test_details = relationship('TableWalkTestDetail', backref='walk_test', cascade='all, delete-orphan')
    technology_type = relationship('TableTechnologyType')
    complaint_type = relationship('TableComplaintType')
    service_type = relationship('TableServiceType')
    problematic_service = relationship('TableProblematicService')
    walk_test_status = relationship('TableWalkTestStatus')

    def __repr__(self):
        return (
            f"<TableWalkTest(id={self.id}, ref_id={self.ref_id}, province={self.province}, "
            f"region={self.region}, city={self.city}, is_village={self.is_village}, "
            f"latitude={self.latitude}, longitude={self.longitude}, serving_cell={self.serving_cell}, "
            f"serving_site={self.serving_site}, walk_test_status_id={self.walk_test_status_id}, technology_type_id={self.technology_type_id}"
            f"problematic_service_id={self.problematic_service_id} service_type_id={self.service_type_id}, created_at={self.created_at})>"
        )
