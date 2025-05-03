from datetime import datetime

from pydantic import BaseModel

from app.domain.enums.sms_status_enum import SmsStatusEnum
from app.interfaces.dto.success_response import BaseSuccessResponse

class GetNLastSmsRecords(BaseModel):
    phone_number : str
    message: str
    status: SmsStatusEnum
    sms_id: str
    updated_at: datetime

class GetNLastSmsRecordsResponse(BaseSuccessResponse[GetNLastSmsRecords]):
    pass