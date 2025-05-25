from abc import ABC, abstractmethod


class SmppService(ABC):

    @abstractmethod
    async def send_sms(self, phone: str, message: str):
        raise NotImplementedError()

    @abstractmethod
    async def listen(self):
        raise NotImplementedError()