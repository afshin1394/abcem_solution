from sqlalchemy import Column, String

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK


class TableServiceType(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_service_type'
    name =  Column(String)