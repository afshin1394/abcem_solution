import uuid

from sqlalchemy import Column, String,  BigInteger, TIMESTAMP
from sqlalchemy.sql import func
from app.infrastructure.schemas.base_db_model import BaseDBModelWithUUIDPK


class TableUsers(BaseDBModelWithUUIDPK):
    __tablename__ = 'table_users'
    name = Column(String)
    age = Column(BigInteger)
    gender = Column(String)
    date_joined = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
