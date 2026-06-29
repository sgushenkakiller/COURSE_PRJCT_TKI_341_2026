from abc import ABC
from abc import abstractmethod

from entities.security_event import SecurityEvent


class MonitorInterface(ABC):

    @abstractmethod
    def notify(self, event: SecurityEvent) -> None:
        ...

    @abstractmethod
    def detect(self, event: SecurityEvent) -> bool:
        ...