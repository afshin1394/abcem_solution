from enum import Enum


class SmsStatusEnum(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"