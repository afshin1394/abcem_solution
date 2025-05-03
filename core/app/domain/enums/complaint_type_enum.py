from enum import Enum

from enum import Enum


class ComplaintTypeEnum(int, Enum):
    # Voice Issues
    POOR_COVERAGE_VOICE = 1
    NO_COVERAGE_VOICE = 2
    VOICE_FADING = 3
    CALL_DROPS_MOVING = 4
    CALL_DROPS_STATIONARY = 5
    MUTE_CALLS = 6
    SHORT_CODE_ISSUE = 7
    CALL_DROPS_4G = 8

    # Data Issues
    POOR_COVERAGE_DATA = 9
    NO_COVERAGE_DATA = 10
    NO_DATA_CONNECTION = 11
    LOW_SPEED = 12

    # Voice & Data Issues
    POOR_COVERAGE_VOICE_DATA = 13
    NO_COVERAGE_VOICE_DATA = 14
    NO_DATA_CONNECTION_VOICE_DATA = 15
    LOW_SPEED_VOICE_DATA = 16
