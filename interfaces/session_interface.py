from abc import ABC, abstractmethod

from entities.access_session import AccessSession


class SessionInterface(ABC):

    @abstractmethod
    def create(self, session: AccessSession) -> None:
        pass

    @abstractmethod
    def close(self, session_id: str) -> None:
        pass

    @abstractmethod
    def get(self, session_id: str) -> AccessSession | None:
        pass