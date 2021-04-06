from api.enums.utils import AutoName
from enum import auto


class OperationalState(AutoName):
    ENABLED = auto()
    DISABLED = auto()


class UsageState(AutoName):
    IN_USE = auto()
    NOT_IN_USE = auto()
