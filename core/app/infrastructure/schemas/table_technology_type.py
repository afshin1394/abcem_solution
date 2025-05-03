from sqlalchemy import Column, String

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK


class TableTechnologyType(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_technology_type'
    name =  Column(String)