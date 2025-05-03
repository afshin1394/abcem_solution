from sqlalchemy import Column, String

from app.infrastructure.schemas.base_db_model import  BaseDBModelWithIntegerPK


class TableComplaintType(BaseDBModelWithIntegerPK):
      __tablename__ = 'table_complaint_type'
      name = Column(String)
