from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repository_impl.read.read_walk_test_repository_impl import ReadWalkTestRepositoryImpl


@pytest.mark.asyncio
@pytest.mark.parametrize("seconds_ago, expected_result", [
    (301, True),   # More than 300 seconds ago
    (299, False),  # Less than 300 seconds ago
])
async def test_validate_walk_test_execution_time(seconds_ago, expected_result):
    # Arrange
    mock_db = AsyncMock()
    service = ReadWalkTestRepositoryImpl(db=mock_db)

    # Create a fake walk_test object
    entered_at = datetime.now(pytz.timezone("Asia/Tehran")) - timedelta(seconds=seconds_ago)
    mock_walk_test = MagicMock()
    mock_walk_test.entered_at = entered_at

    # Properly mock execute().scalars().one_or_none()
    mock_scalar_result = AsyncMock()
    mock_scalar_result.one_or_none.return_value = mock_walk_test

    mock_execute_result = AsyncMock()
    mock_execute_result.scalars.return_value = mock_scalar_result

    mock_db.execute.return_value = mock_execute_result

    # Act
    result = await service.validate_walk_test_execution_time("test-id")

    # Assert
    assert result == expected_result