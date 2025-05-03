from enum import Enum

class ProblematicServiceEnum(int, Enum):
    VOICE = 1
    DATA = 2
    VOICE_AND_DATA = 3