from abc import ABC, abstractmethod


class SMSService(ABC):
    @abstractmethod
    async def send_sms(self, msisdn: str, otp: str):
        pass

