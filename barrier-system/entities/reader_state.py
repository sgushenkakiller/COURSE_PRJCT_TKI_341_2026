from enum import Enum


class ReaderState(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    READY = "ready"
    DISABLED = "disabled"
    ERROR = "error"
