from dataclasses import dataclass, field
from datetime import datetime

from .policy_result import PolicyResult


@dataclass(slots=True, frozen=True)
class AccessDecision:
    """
    Решение, принятое Policy Engine.
    """

    request_id: str

    result: PolicyResult

    reason: str

    timestamp: datetime = field(default_factory=datetime.utcnow)

    operator_required: bool = False

    administrator_required: bool = False