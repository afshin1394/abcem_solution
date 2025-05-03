from abc import ABC, abstractmethod
from typing import Tuple


class GISService(ABC):
    @abstractmethod
    async def validate_location_within_offset(self, offset=50, **coords) -> bool:
        pass

