from abc import ABC, abstractmethod


class ReadProblematicServiceRepository(ABC):
    @abstractmethod
    async def get_all(self):
        pass