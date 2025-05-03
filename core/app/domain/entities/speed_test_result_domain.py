from dataclasses import dataclass
from app.domain.enums.technology_enum import TechnologyEnum


@dataclass
class SpeedTestResultDomain:
    walk_test_detail_id: str
    download: float
    upload: float
    ping: float
    jitter: float
    technology_id: TechnologyEnum
