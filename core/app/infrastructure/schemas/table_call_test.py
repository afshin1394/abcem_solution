
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK


class TableCallTest(BaseDBModelWithUUIDPK):
    __tablename__ = 'table_call_test'
    drop_call = Column(Integer)
    is_voltE = Column(Boolean)
    technology_id = Column(Integer, ForeignKey('table_technology_type.id'))
    walk_test_detail_id = Column(String,ForeignKey('table_walk_test_detail.id'))

    technology = relationship("TableTechnologyType")
