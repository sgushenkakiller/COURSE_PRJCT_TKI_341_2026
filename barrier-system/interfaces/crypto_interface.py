from abc import ABC, abstractmethod


class CryptoInterface(ABC):

    @abstractmethod
    def hash(self, value: str) -> str:
        pass

    @abstractmethod
    def verify(self, value: str, digest: str) -> bool:
        pass