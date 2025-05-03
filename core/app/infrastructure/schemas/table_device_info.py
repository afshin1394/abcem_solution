
from sqlalchemy import DateTime, Column, Integer, String, ForeignKey
from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK



class TableDeviceInfo(BaseDBModelWithUUIDPK):
    __tablename__ = 'table_device_info'
    security_patch = Column(DateTime, nullable=False)
    sdk = Column(Integer, nullable=False)
    os_version = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    device = Column(String, nullable=False)
    hardware = Column(String, nullable=False)
    model = Column(String, nullable=False)
    walk_test_id = Column(String,ForeignKey('table_walk_test.id'), nullable=False)

