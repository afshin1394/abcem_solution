from sqlalchemy import Column, String

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK


class TableProblematicService(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_problematic_service'
    name = Column(String)