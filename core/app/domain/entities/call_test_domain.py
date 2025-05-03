from dataclasses import dataclass

from app.domain.enums.technology_enum import TechnologyEnum


@dataclass
class CallTestDomain:
     walk_test_detail_id : str
     drop_call : int
     is_voltE : bool
     technology_id : TechnologyEnum