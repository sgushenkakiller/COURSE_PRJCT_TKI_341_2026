from entities.security_event import SecurityEvent
from entities.security_event_type import SecurityEventType
from entities.severity import Severity


class AnomalyDetector:

    def detect(
        self,
        event: SecurityEvent
    ) -> bool:

        if event.severity == Severity.CRITICAL:
            return True

        if event.event_type == SecurityEventType.POLICY_VIOLATION:
            return True

        if event.event_type == SecurityEventType.SYSTEM_ERROR:
            return True

        return False