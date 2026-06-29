from enum import Enum


class CommandResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    UNSUPPORTED = "unsupported"