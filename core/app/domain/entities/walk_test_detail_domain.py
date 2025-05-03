from dataclasses import dataclass

from app.domain.enums.step_test_type_enum import StepTestTypeEnum


@dataclass
class WalkTestDetailDomain:
    id: str
    step_number : int
    step_type_id : StepTestTypeEnum
    walk_test_id : str