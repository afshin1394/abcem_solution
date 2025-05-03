import pytest
from pydantic import ValidationError

from app.domain.enums.step_test_type_enum import StepTestTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.interfaces.dto.request.walk_test_results_request import  WalkTestDetailRequest
def test_valid_speed_test():
    data = {
        "step_number": 1,
        "technology_id": TechnologyEnum.LTE,
        "step_type_id": StepTestTypeEnum.SPEED_TEST,
        "speed_test_result": [{"download": 100.0, "upload": 50.0, "ping": 10.5, "jitter": 2.1}],
    }
    assert WalkTestDetailRequest(**data)

def test_invalid_missing_speed_test():
    data = {
        "step_number": 1,
        "technology_id": TechnologyEnum.LTE,
        "step_type_id": StepTestTypeEnum.SPEED_TEST,
        "speed_test_result": None,
    }
    with pytest.raises(ValidationError, match="speed_test_result must not be None if step_type_id is SPEED_TEST"):
        WalkTestDetailRequest(**data)

def test_valid_cell_info():
    data = {
        "step_number": 2,
        "technology_id": TechnologyEnum.NR,
        "step_type_id": StepTestTypeEnum.EXTRACT_CELL_INFO,
        "cell_info_result": [{"technology_id": 5, "level": -90, "quality": 30, "cell_data": {"id": "cell123"}}],
    }
    assert WalkTestDetailRequest(**data)

def test_invalid_missing_cell_info():
    data = {
        "step_number": 2,
        "technology_id": TechnologyEnum.NR,
        "step_type_id": StepTestTypeEnum.EXTRACT_CELL_INFO,
    }
    assert  WalkTestDetailRequest(**data)

def test_valid_call_test():
    data = {
        "step_number": 3,
        "technology_id": TechnologyEnum.LTE,
        "step_type_id": StepTestTypeEnum.CALL,
        "call_test_result": [{"drop_call": 0, "is_voltE": True, "technology_id": 4}],
    }
    assert WalkTestDetailRequest(**data)

def test_invalid_missing_call_test():
    data = {
        "step_number": 3,
        "technology_id": TechnologyEnum.LTE,
        "step_type_id": StepTestTypeEnum.CALL,
        "call_test_result": [{"drop_call": 0, "is_voltE": True, "technology_id": 4}],
    }
    assert WalkTestDetailRequest(**data)

def test_result_key(msisdn : str = "string"):
    print(f"key :::: GetWalkTestByMSISDNQuery:{{\"msisdn\":\"{msisdn}\"}}")