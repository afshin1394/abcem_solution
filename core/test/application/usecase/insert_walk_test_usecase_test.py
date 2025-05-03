import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock

from app.application.feature.commands.create_walk_test_results_command import CreateWalkTestResultsCommand
from app.application.usecase.insert_walk_test_results_use_case import InsertWalkTestResultsUseCase
from app.interfaces.dto.request.walk_test_results_request import WalkTestResultsRequest


@pytest.mark.asyncio
async def test_convert_walk_test_results_request_to_command():
    # Create mock WalkTestResultsRequest
    mock_request = MagicMock(spec=WalkTestResultsRequest)
    mock_request.walk_test_id = str(uuid.uuid4())

    # Create mock step
    mock_step = MagicMock()
    mock_step.step_number = 1
    mock_step.step_type_id = "some_step_type"

    # Mock speed test results
    mock_speed_test = MagicMock()
    mock_speed_test.download = 50.0
    mock_speed_test.upload = 10.0
    mock_speed_test.ping = 30.0
    mock_speed_test.jitter = 5.0
    mock_step.speed_test_result = [mock_speed_test]

    # Mock cell info results
    mock_cell_info = MagicMock()
    mock_cell_info.technology_id = "4G"
    mock_cell_info.level = -90
    mock_cell_info.quality = 30
    mock_cell_info.cell_data = "some_data"
    mock_step.cell_info_result = [mock_cell_info]

    # Mock call test results
    mock_call_test = MagicMock()
    mock_call_test.drop_call = False
    mock_call_test.is_voltE = True
    mock_call_test.technology_id = "5G"
    mock_step.call_test_result = [mock_call_test]

    # Assign the mocked steps list
    mock_request.steps = [mock_step]

    # Call the static method
    command = await InsertWalkTestResultsUseCase.convert_walk_test_results_request_to_command(mock_request)

    # Assertions
    assert isinstance(command, CreateWalkTestResultsCommand)
    assert len(command.walk_test_detail_list) == 1
    assert len(command.speed_test_list) == 1
    assert len(command.cell_info_list) == 1
    assert len(command.call_test_list) == 1

    # Validate data mapping
    assert command.walk_test_detail_list[0].walk_test_id == mock_request.walk_test_id
    assert command.walk_test_detail_list[0].step_number == mock_step.step_number
    assert command.speed_test_list[0].download == mock_speed_test.download
    assert command.cell_info_list[0].technology_id == mock_cell_info.technology_id
    assert command.call_test_list[0].is_voltE == mock_call_test.is_voltE


    print(command.__str__())



@pytest.mark.asyncio
async def test_convert_walk_test_results_request_to_command():
    # Create mock WalkTestResultsRequest
    mock_request = MagicMock(spec=WalkTestResultsRequest)
    mock_request.walk_test_id = str(uuid.uuid4())

    # Create mock step 1
    mock_step1 = MagicMock()
    mock_step1.step_number = 1
    mock_step1.step_type_id = "step_type_1"

    # Create mock step 2
    mock_step2 = MagicMock()
    mock_step2.step_number = 2
    mock_step2.step_type_id = "step_type_2"

    # Mock speed test results for both steps
    mock_speed_test1 = MagicMock()
    mock_speed_test1.download = 50.0
    mock_speed_test1.upload = 10.0
    mock_speed_test1.ping = 30.0
    mock_speed_test1.jitter = 5.0

    mock_speed_test2 = MagicMock()
    mock_speed_test2.download = 70.0
    mock_speed_test2.upload = 15.0
    mock_speed_test2.ping = 25.0
    mock_speed_test2.jitter = 4.0

    mock_step1.speed_test_result = [mock_speed_test1, mock_speed_test2]
    mock_step2.speed_test_result = [mock_speed_test2]

    # Mock cell info results for both steps
    mock_cell_info1 = MagicMock()
    mock_cell_info1.technology_id = "4G"
    mock_cell_info1.level = -90
    mock_cell_info1.quality = 30
    mock_cell_info1.cell_data = "data1"

    mock_cell_info2 = MagicMock()
    mock_cell_info2.technology_id = "5G"
    mock_cell_info2.level = -85
    mock_cell_info2.quality = 40
    mock_cell_info2.cell_data = "data2"

    mock_step1.cell_info_result = [mock_cell_info1, mock_cell_info2]
    mock_step2.cell_info_result = [mock_cell_info2]

    # Mock call test results for both steps
    mock_call_test1 = MagicMock()
    mock_call_test1.drop_call = False
    mock_call_test1.is_voltE = True
    mock_call_test1.technology_id = "5G"

    mock_call_test2 = MagicMock()
    mock_call_test2.drop_call = True
    mock_call_test2.is_voltE = False
    mock_call_test2.technology_id = "4G"

    mock_step1.call_test_result = [mock_call_test1, mock_call_test2]
    mock_step2.call_test_result = [mock_call_test2]

    # Assign the mocked steps list
    mock_request.steps = [mock_step1, mock_step2]

    # Call the static method
    command = await InsertWalkTestResultsUseCase.convert_walk_test_results_request_to_command(mock_request)

    # Assertions
    assert isinstance(command, CreateWalkTestResultsCommand)
    assert len(command.walk_test_detail_list) == 2  # Two steps
    assert len(command.speed_test_list) >= 2  # At least two speed test results
    assert len(command.cell_info_list) >= 2  # At least two cell info results
    assert len(command.call_test_list) >= 2  # At least two call test results

    # Validate data mapping
    assert command.walk_test_detail_list[0].step_number == mock_step1.step_number
    assert command.speed_test_list[0].download == mock_speed_test1.download
    assert command.cell_info_list[0].technology_id == mock_cell_info1.technology_id
    assert command.call_test_list[0].is_voltE == mock_call_test1.is_voltE

    print(command.__dict__)





@pytest.mark.asyncio
async def test_walk_test_detail_id_consistency():
    # Create mock WalkTestResultsRequest
    mock_request = MagicMock(spec=WalkTestResultsRequest)
    mock_request.walk_test_id = str(uuid.uuid4())

    # Create mock step 1
    mock_step1 = MagicMock()
    mock_step1.step_number = 1
    mock_step1.step_type_id = "step_type_1"

    # Create mock step 2
    mock_step2 = MagicMock()
    mock_step2.step_number = 2
    mock_step2.step_type_id = "step_type_2"

    # Mock speed test results for both steps
    mock_speed_test1 = MagicMock()
    mock_speed_test2 = MagicMock()
    mock_step1.speed_test_result = [mock_speed_test1]
    mock_step2.speed_test_result = [mock_speed_test2]

    # Mock cell info results for both steps
    mock_cell_info1 = MagicMock()
    mock_cell_info2 = MagicMock()
    mock_step1.cell_info_result = [mock_cell_info1]
    mock_step2.cell_info_result = [mock_cell_info2]

    # Mock call test results for both steps
    mock_call_test1 = MagicMock()
    mock_call_test2 = MagicMock()
    mock_step1.call_test_result = [mock_call_test1]
    mock_step2.call_test_result = [mock_call_test2]

    # Assign the mocked steps list
    mock_request.steps = [mock_step1, mock_step2]

    # Call the static method
    command = await InsertWalkTestResultsUseCase.convert_walk_test_results_request_to_command(mock_request)

    # Extract walk_test_detail_ids from each list
    walk_test_detail_ids = [detail.id for detail in command.walk_test_detail_list]

    # Check if all associated items in speed_test_list, cell_info_list, and call_test_list have matching walk_test_detail_id
    for speed_test in command.speed_test_list:
        assert speed_test.walk_test_detail_id in walk_test_detail_ids, "SpeedTestResult walk_test_detail_id mismatch"

    for cell_info in command.cell_info_list:
        assert cell_info.walk_test_detail_id in walk_test_detail_ids, "CellInfo walk_test_detail_id mismatch"

    for call_test in command.call_test_list:
        assert call_test.walk_test_detail_id in walk_test_detail_ids, "CallTest walk_test_detail_id mismatch"

    # Ensure each list has matching indices for their walk_test_detail_id
    for i, detail in enumerate(command.walk_test_detail_list):
        # Check if corresponding entities in the same index share the same ID
        if i < len(command.speed_test_list):
            assert command.speed_test_list[i].walk_test_detail_id == detail.id, "SpeedTest ID mismatch at index " + str(i)
        if i < len(command.cell_info_list):
            assert command.cell_info_list[i].walk_test_detail_id == detail.id, "CellInfo ID mismatch at index " + str(i)
        if i < len(command.call_test_list):
            assert command.call_test_list[i].walk_test_detail_id == detail.id, "CallTest ID mismatch at index " + str(i)




@pytest.mark.asyncio
async def test_walk_test_detail_id_consistency_and_uniqueness():
    # Create mock WalkTestResultsRequest
    mock_request = MagicMock(spec=WalkTestResultsRequest)
    mock_request.walk_test_id = str(uuid.uuid4())

    # Create mock step 1
    mock_step1 = MagicMock()
    mock_step1.step_number = 1
    mock_step1.step_type_id = "step_type_1"

    # Create mock step 2
    mock_step2 = MagicMock()
    mock_step2.step_number = 2
    mock_step2.step_type_id = "step_type_2"

    # Mock speed test results for both steps
    mock_speed_test1 = MagicMock()
    mock_speed_test2 = MagicMock()
    mock_step1.speed_test_result = [mock_speed_test1]
    mock_step2.speed_test_result = [mock_speed_test2]

    # Mock cell info results for both steps
    mock_cell_info1 = MagicMock()
    mock_cell_info2 = MagicMock()
    mock_step1.cell_info_result = [mock_cell_info1]
    mock_step2.cell_info_result = [mock_cell_info2]

    # Mock call test results for both steps
    mock_call_test1 = MagicMock()
    mock_call_test2 = MagicMock()
    mock_step1.call_test_result = [mock_call_test1]
    mock_step2.call_test_result = [mock_call_test2]

    # Assign the mocked steps list
    mock_request.steps = [mock_step1, mock_step2]

    # Call the static method
    command = await InsertWalkTestResultsUseCase.convert_walk_test_results_request_to_command(mock_request)

    # Extract walk_test_detail_ids from WalkTestDetailDomain
    walk_test_detail_ids = [detail.id for detail in command.walk_test_detail_list]

    # Ensure all walk_test_detail_ids are unique
    assert len(walk_test_detail_ids) == len(set(walk_test_detail_ids)), "walk_test_detail_ids should be unique"

    # Ensure each list has matching indices for their walk_test_detail_id
    for i, detail in enumerate(command.walk_test_detail_list):
        # Check if corresponding entities in the same index share the same ID
        if i < len(command.speed_test_list):
            assert command.speed_test_list[i].walk_test_detail_id == detail.id, f"SpeedTest ID mismatch at index {i}"
        if i < len(command.cell_info_list):
            assert command.cell_info_list[i].walk_test_detail_id == detail.id, f"CellInfo ID mismatch at index {i}"
        if i < len(command.call_test_list):
            assert command.call_test_list[i].walk_test_detail_id == detail.id, f"CallTest ID mismatch at index {i}"

    # Ensure different indices have different IDs
    for i in range(len(walk_test_detail_ids) - 1):
        assert walk_test_detail_ids[i] != walk_test_detail_ids[i + 1], f"walk_test_detail_id at index {i} and {i+1} should be different"
