from enum import Enum


class Command(Enum):
    OPEN_BARRIER = "open_barrier"
    CLOSE_BARRIER = "close_barrier"
    DENY_ACCESS = "deny_access"
    LOG_EVENT = "log_event"