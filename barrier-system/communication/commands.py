from enum import Enum


class Command(Enum):
    ACCESS_REQUEST = "access_request"
    OPEN_BARRIER = "open_barrier"
    CLOSE_BARRIER = "close_barrier"
    STOP_BARRIER = "stop_barrier"
    LOCK_BARRIER = "lock_barrier"
    UNLOCK_BARRIER = "unlock_barrier"

    ALLOW_ACCESS = "allow_access"
    DENY_ACCESS = "deny_access"

    LOG_EVENT = "log_event"

    HEALTH_CHECK = "health_check"

    HEARTBEAT = "heartbeat"