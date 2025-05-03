"""Declaring base model classes for sqlalchemy models."""
import uuid
from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, String, Integer, MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base


Base = declarative_base(metadata=MetaData(schema="core_service"))

# Create a base class that uses the metadata and specify the schema in the Table definitions
class BaseDBModelWithUUIDPK(Base):
    __abstract__ = True  # <-- Prevent table creation for BaseDBModel
    """Class defining common db model components."""
    # autoinc pk key
    __table_args__ = {"schema": "core_service"}

    id = Column(String, primary_key=True,default=lambda: str(uuid.uuid4()))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tehran')))
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    # refresh server defaults with asyncio
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

class BaseDBModelWithIntegerPK(Base):
    __abstract__ = True
    __table_args__ = {"schema": "core_service"}

    id = Column(Integer, primary_key=True,autoincrement=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tehran')))
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


    __mapper_args__ = {"eager_defaults": True}
