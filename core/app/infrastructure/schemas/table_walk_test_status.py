from sqlalchemy import String, Column

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK


class TableWalkTestStatus(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_walk_test_status'
    name= Column(String,nullable=False)