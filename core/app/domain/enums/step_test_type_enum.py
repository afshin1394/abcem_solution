from enum import Enum

class StepTestTypeEnum(int, Enum):
    CALL = 1
    SPEED_TEST = 2
    EXTRACT_CELL_INFO = 3