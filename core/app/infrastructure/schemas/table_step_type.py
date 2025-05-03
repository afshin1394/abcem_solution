from sqlalchemy import String, Column

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK


class TableStepTestType(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_step_test_type'
    name = Column(String)