from enum import Enum


class SecurityEventType(Enum):
    ACCESS_REQUEST = "access_request"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"

    INVALID_CARD = "invalid_card"
    BLOCKED_USER = "blocked_user"

    POLICY_VIOLATION = "policy_violation"

    DEVICE_CONNECTED = "device_connected"
    DEVICE_DISCONNECTED = "device_disconnected"

    SYSTEM_ERROR = "system_error"

    BARRIER_OPENED = "barrier_opened"
    BARRIER_CLOSED = "barrier_closed"

    LOGIN = "login"
    LOGOUT = "logout"