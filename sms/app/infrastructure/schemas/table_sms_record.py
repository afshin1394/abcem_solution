
from sqlalchemy import Column,  String, Enum

from app.infrastructure.schemas.base_db_model import BaseDBModelWithIntegerPK
from app.domain.enums.sms_status_enum import SmsStatusEnum


class TableSmsRecord(BaseDBModelWithIntegerPK):
    __tablename__ = 'table_sms_record'
    phone_number = Column(String, nullable=False)
    message = Column(String, nullable=False)
    status = Column(Enum(SmsStatusEnum), default=SmsStatusEnum.SENT)
    sms_id = Column(String, nullable=False)

