from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK


class TableSpeedTestResults(BaseDBModelWithUUIDPK):
       __tablename__ = 'table_speed_test_results'

       download = Column(Float, default=0.0,nullable=False)
       upload = Column(Float, default=0.0,nullable=False)
       ping = Column(Float, default=0.0,nullable=False)
       jitter = Column(Float, default=0.0,nullable=False)
       technology_id = Column(Integer, ForeignKey('table_technology_type.id'))
       walk_test_detail_id = Column(String, ForeignKey('table_walk_test_detail.id'))

       technology = relationship('TableTechnologyType')

