from sqlalchemy import Column, String, Text

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK


class TableBaseConfig(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_base_config'
    name = Column(String, nullable=False)
    value = Column(String,nullable=False)
    scale = Column(String, nullable=False)
