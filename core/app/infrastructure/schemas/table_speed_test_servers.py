
from sqlalchemy import Column, String, TIMESTAMP, FLOAT

from app.infrastructure.schemas.base_db_model import  BaseDBModelWithIntegerPK


class TableSpeedTestServer(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_speed_test_servers'
    name = Column(String, nullable=True)
    sponsor = Column(String, nullable=True)
    country = Column(String, nullable=True)
    lat = Column(String, nullable=True)
    lon = Column(String, nullable=True)
    host = Column(String, nullable=True)
    distance = Column(FLOAT, nullable=True)
    url = Column(String, nullable=True)



