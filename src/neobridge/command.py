from enum import Enum

class Command(Enum):
    SHOW = -3
    RESET = -2
    WAIT_FOR_RESPONSE = -1
    
    SET_ALL = 0
    SET_ONE = 1
    SET_TO_LIST = 2