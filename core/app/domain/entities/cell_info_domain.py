from dataclasses import dataclass
from typing import Dict, Any

from app.domain.enums.technology_enum import TechnologyEnum


@dataclass
class CellInfoDomain:
    walk_test_detail_id: str
    technology_id: TechnologyEnum
    level: int
    quality: int
    cell_data: Dict[str, Any]