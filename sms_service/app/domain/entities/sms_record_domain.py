from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.domain.enums.sms_status_enum import SmsStatusEnum


class SMSRecordDomain(BaseModel):
    phone_number : str
    message: str
    status: SmsStatusEnum
    updated_at: Optional[datetime] = None
    sms_id : str = None



    def __repr__(self):
        return (
            f"SMSRecordDomain(sms_id={self.sms_id!r}, "
            f"phone_number={self.phone_number!r}, "
            f"status={self.status.value!r}, "
            f"updated_at={self.updated_at.isoformat()})"
            f"sms_id={self.sms_id})"
        )