from abc import ABC, abstractmethod


class DeviceInterface(ABC):

    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def enable(self) -> None:
        pass

    @abstractmethod
    def disable(self) -> None:
        pass

    @abstractmethod
    def enabled(self) -> bool:
        pass