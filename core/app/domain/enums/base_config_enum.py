from enum import Enum


class BaseConfigEnum(str, Enum):
    WALK_TEST_LOCATION_OFFSET = "walk_test_location_offset"
    WALK_TEST_VALIDATION_DURATION = "walk_test_validation_duration"