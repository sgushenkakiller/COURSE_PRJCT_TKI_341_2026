from abc import ABC, abstractmethod

from entities.user import User


class AuthorizationInterface(ABC):

    @abstractmethod
    def authorize(self, user: User) -> bool:
        pass