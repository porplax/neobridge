from enum import Enum

class Command(Enum):
    RESET = -2
    WAIT_FOR_RESPONSE = -1
    
    SET_ALL = 0
    SET_ONE = 1
    SHOW = 2