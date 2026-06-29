from abc import ABC, abstractmethod

from entities.security_event import SecurityEvent


class MonitorInterface(ABC):

    @abstractmethod
    def notify(self, event: SecurityEvent) -> None:
        pass

    @abstractmethod
    def detect(self, event: SecurityEvent) -> bool:
        pass
