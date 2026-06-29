from abc import ABC
from abc import abstractmethod

from entities.access_request import AccessRequest
from entities.reader_state import ReaderState


class ReaderInterface(ABC):

    @abstractmethod
    def read(self) -> AccessRequest | None:
        ...

    @abstractmethod
    def identifier(self) -> str:
        ...

    @abstractmethod
    def state(self) -> ReaderState:
        ...