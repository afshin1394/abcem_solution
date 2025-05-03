from typing import Optional, Any, Dict

from pydantic import BaseModel, model_validator, Field, ConfigDict

from app.domain.enums.step_test_type_enum import StepTestTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from collections import OrderedDict


class SpeedTestResultRequest(BaseModel):
    download: float
    upload: float
    ping: float
    jitter: float
    technology_id : TechnologyEnum


class CallTestResultRequest(BaseModel):
    drop_call: int
    is_voltE: bool
    technology_id: TechnologyEnum


class CellInfoResultRequest(BaseModel):
    technology_id: TechnologyEnum
    level: int
    quality: int
    cell_data: Dict[str, Any]


class WalkTestDetailRequest(BaseModel):
    step_number: int = Field(default=1)
    step_type_id: StepTestTypeEnum
    speed_test_result: Optional[list[SpeedTestResultRequest]] = None
    cell_info_result: Optional[list[CellInfoResultRequest]] = None
    call_test_result: Optional[list[CallTestResultRequest]] = None

    @model_validator(mode='after')
    def validate_step_type_fields(self):
        step_type_id = self.step_type_id
        speed_test_result = self.speed_test_result
        cell_info_result = self.cell_info_result
        call_test_result = self.call_test_result

        if step_type_id == StepTestTypeEnum.SPEED_TEST and not speed_test_result:
            raise ValueError("speed_test_result must not be None if step_test_type_id is SPEED_TEST = 2")
        if step_type_id == StepTestTypeEnum.EXTRACT_CELL_INFO and not cell_info_result:
            raise ValueError("cell_info_result must not be None if step_test_type_id is EXTRACT_CELL_INFO = 3")
        if step_type_id == StepTestTypeEnum.CALL and not call_test_result:
            raise ValueError("call_test_result must not be None if step_test_type_id is CALL = 1")

        return self


class WalkTestResultsRequest(BaseModel):
    walk_test_id: str
    steps: list[WalkTestDetailRequest]

    @model_validator(mode="after")  # Ensure validation happens after parsing
    def validate_step_numbers(self):
        if not self.steps:
            raise ValueError("Steps cannot be empty.")

        step_numbers = [step.step_number for step in self.steps]

        if step_numbers[0] != 1:
            raise ValueError("Step numbering must start from 1.")

        for i in range(1, len(step_numbers)):
            if step_numbers[i] != step_numbers[i - 1] + 1:
                raise ValueError(f"Step number {step_numbers[i]} is not sequential after {step_numbers[i - 1]}.")

        return self # Return the validated steps

    @model_validator(mode="after")
    def validate_walk_test_id(self):
        if self.walk_test_id is None:
            raise ValueError("you must provide walk test id")
        return self


    model_config = ConfigDict(populate_by_name=True,json_schema_extra={
        "example": {
            "walk_test_id": "db5c3630-d87b-42d4-9481-b8482a916085",
            "steps": [
                {
                    "step_number": 1,
                    "step_type_id": 2,
                    "speed_test_result": [
                        {
                            "download": 50.5,
                            "upload": 25.2,
                            "ping": 30.1,
                            "jitter": 5.0,
                            "technology_id": 4
                        }
                    ],
                    "cell_info_result": None,
                    "call_test_result": None
                },
                {
                    "step_number": 2,
                    "step_type_id": 3,
                    "speed_test_result": None,
                    "cell_info_result": [
                        {
                            "technology_id": 4,
                            "level": -75,
                            "quality": 85,
                            "cell_data": {
                                "RSCP": -90,
                                "ECNO": -10,
                                "RSRQ": -11,
                                "RSRP": -105
                            }
                        }
                    ],
                    "call_test_result": None
                },
                {
                    "step_number": 3,
                    "step_type_id": 1,
                    "speed_test_result": None,
                    "cell_info_result": None,
                    "call_test_result": [
                        {
                            "drop_call": 0,
                            "is_voltE": False,
                            "technology_id": 4
                        }
                    ]
                }
            ]
        }
    })
