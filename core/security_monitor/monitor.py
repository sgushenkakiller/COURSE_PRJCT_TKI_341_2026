from entities.security_event import SecurityEvent

from interfaces.monitor_interface import MonitorInterface

from .anomaly_detector import AnomalyDetector
from .event_handler import EventHandler


class SecurityMonitor(MonitorInterface):

    def __init__(self) -> None:
        self._detector = AnomalyDetector()
        self._handler = EventHandler()

    def notify(self, event: SecurityEvent) -> None:
        self._handler.handle(event)

        if self._detector.detect(event):
            self.on_anomaly(event)

    def detect(self, event: SecurityEvent) -> bool:
        return self._detector.detect(event)

    def on_anomaly(self, event: SecurityEvent) -> None:
        pass

    def events(self) -> list[SecurityEvent]:
        return self._handler.events()

    def clear(self) -> None:
        self._handler.clear()

    def count(self) -> int:
        return self._handler.count()

    def get_active_sessions(self) -> list:
        return []
