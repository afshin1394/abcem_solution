from dataclasses import dataclass

import pytest
import asyncio
from datetime import time

from sqlalchemy import Column, Integer

from app.domain.entities.walk_test_domain import WalkTestDomain
from app.domain.enums.complaint_type_enum import ComplaintTypeEnum
from app.domain.enums.problematic_service_enum import ProblematicServiceEnum
from app.domain.enums.service_type_enum import ServiceTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum
from app.infrastructure.mapper.mapper import map_models, map_models_list
from app.infrastructure.schemas.table_walk_test import TableWalkTest


@dataclass
class A:
    name: str
    datetime: time


@dataclass
class B:
    name: str
    datetime: time


@dataclass
class C:
    name: str
    type: ServiceTypeEnum


@dataclass
class D:
    name = str
    type = Column(Integer)


@pytest.mark.asyncio
async def test_date_mapper():
    a: A = A(name="afshin", datetime=time.fromisoformat("10:18:25"))
    print(await map_models(a, B))


@pytest.mark.asyncio
async def test_time_mapper():
    a: A = A(name="ali", datetime=time.fromisoformat("00:02:334Z"))
    print(await map_models(a, B))


@pytest.mark.asyncio
async def test_enum_mapper():
    c: C = C(name="ali", type=ServiceTypeEnum.FDD)
    print(await map_models(c, D))


@pytest.mark.asyncio
async def test_enum_mapper():
    # Example WalkTestDomain instance
    walk_test_domain = WalkTestDomain(
        ref_id="string",
        province="string",
        region="string",
        city="string",
        is_village=True,
        latitude=0.0,
        longitude=0.0,
        serving_cell="string",
        serving_site="string",
        is_at_all_hours=True,
        start_time_of_issue=time.fromisoformat("13:28:35.463000+00:00"),
        end_time_of_issue=time.fromisoformat("13:28:35.463000+00:00"),
        msisdn="string",
        technology_type_id=TechnologyEnum.NR,  # Enum
        complaint_type_id=ComplaintTypeEnum.POOR_COVERAGE_VOICE,  # Enum
        problematic_service_id=ProblematicServiceEnum.VOICE,  # Enum
        service_type_id=ServiceTypeEnum.FDD,  # Enum
        related_tt="string",
        walk_test_status_id=WalkTestStatusEnum.created  # Enum
    )
    print(await map_models(walk_test_domain, TableWalkTest))


import pytest
from app.infrastructure.schemas.table_cell_info import TableCellInfo  # Import the SQLAlchemy model

# Sample data for testing
sample_data = {
    "walk_test_detail_id": "test_walk_test_id",
    "technology_id": 1,  # Assuming TechnologyEnum is an int-based Enum
    "level": 2,
    "quality": 3,
    "cell_data": {"key1": "value1", "key2": "value2"},
}

@pytest.mark.asyncio
async def test_map_models():
    # Test the conversion from Dict to TableCellInfo
    cell_info = await map_models(sample_data, TableCellInfo)

    print(cell_info.__dict__)

    # Check that the model is correctly populated
    assert cell_info.walk_test_detail_id == sample_data["walk_test_detail_id"]
    assert cell_info.technology_id == sample_data["technology_id"]
    assert cell_info.level == sample_data["level"]
    assert cell_info.quality == sample_data["quality"]
    assert cell_info.cell_data == sample_data["cell_data"]  # Check if Dict is correctly assigned to JSONB

@pytest.mark.asyncio
async def test_map_models_list():
    # Test the conversion of a list of Dicts to a list of TableCellInfo instances
    data_list = [sample_data, sample_data]  # You can add more data as needed
    cell_info_list = await map_models_list(data_list, TableCellInfo)

    # Check that the length of the returned list matches
    assert len(cell_info_list) == len(data_list)

    # Check that each model is correctly populated
    for cell_info, data in zip(cell_info_list, data_list):
        assert cell_info.walk_test_detail_id == data["walk_test_detail_id"]
        assert cell_info.technology_id == data["technology_id"]
        assert cell_info.level == data["level"]
        assert cell_info.quality == data["quality"]
        assert cell_info.cell_data == data["cell_data"]  # Check if Dict is correctly assigned to JSONB
    for data in cell_info_list:
     print(data.__dict__)