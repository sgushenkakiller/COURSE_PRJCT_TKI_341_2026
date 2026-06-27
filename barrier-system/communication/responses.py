from enum import Enum


class Response(Enum):
    SUCCESS = "success"
    FAILURE = "failure"

    ACCEPTED = "accepted"
    REJECTED = "rejected"

    INVALID = "invalid"

    TIMEOUT = "timeout"

    UNAUTHORIZED = "unauthorized"

    DEVICE_ERROR = "device_error"

    POLICY_VIOLATION = "policy_violation"