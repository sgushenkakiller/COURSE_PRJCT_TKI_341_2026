from abc import ABC, abstractmethod

from entities.security_event import SecurityEvent


class EventHandlerInterface(ABC):

    @abstractmethod
    def handle(self, event: SecurityEvent) -> None:
        pass