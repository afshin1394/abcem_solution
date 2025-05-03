from sqlalchemy import Integer, Column, ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK


class TableCellInfo(BaseDBModelWithUUIDPK):
    __tablename__ = 'table_cell_info'
    cell_data = Column(JSONB)
    level = Column(Integer)
    quality = Column(Integer)
    walk_test_detail_id = Column(String,ForeignKey('table_walk_test_detail.id'))
    technology_id = Column(Integer,ForeignKey('table_technology_type.id'))

    technology = relationship('TableTechnologyType')
