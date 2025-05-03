from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, DateTime, MetaData
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base(metadata=MetaData(schema="sms_service"))

class BaseDBModelWithIntegerPK(Base):
    __abstract__ = True
    __table_args__ = {"schema": "sms_service"}

    id = Column(Integer, primary_key=True,autoincrement=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tehran')))
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


    __mapper_args__ = {"eager_defaults": True}
