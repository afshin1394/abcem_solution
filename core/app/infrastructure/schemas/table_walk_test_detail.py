
from sqlalchemy import Integer, Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK


class TableWalkTestDetail(BaseDBModelWithUUIDPK):
    __tablename__ = 'table_walk_test_detail'
    step_number = Column(Integer)
    step_type_id = Column(Integer,ForeignKey('table_step_test_type.id'))
    walk_test_id = Column(String, ForeignKey('table_walk_test.id'),nullable=False)

    step_test_type = relationship('TableStepTestType')
