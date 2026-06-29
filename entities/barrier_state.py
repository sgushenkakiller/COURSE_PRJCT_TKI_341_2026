from enum import Enum


class BarrierState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    OPENING = "opening"
    CLOSING = "closing"
    STOPPED = "stopped"
    BLOCKED = "blocked"
    FAULT = "fault"
