from dataclasses import dataclass, field
from datetime import datetime

from entities.security_event_type import SecurityEventType
from entities.severity import Severity


@dataclass(slots=True)
class SecurityEvent:

    event_type: SecurityEventType

    source: str

    description: str

    severity: Severity

    timestamp: datetime = field(default_factory=datetime.utcnow)

    request_id: str | None = None

    user_id: str | None = None

    handled: bool = False