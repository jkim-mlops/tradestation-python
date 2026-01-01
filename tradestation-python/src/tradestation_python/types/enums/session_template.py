from enum import Enum


class SessionTemplate(Enum):
    USEQ_PRE = "USEQPre"
    USEQ_POST = "USEQPost"
    USEQ_PRE_AND_POST = "USEQPreAndPost"
    USEQ_24_HOUR = "USEQ24Hour"
    DEFAULT = "Default"
