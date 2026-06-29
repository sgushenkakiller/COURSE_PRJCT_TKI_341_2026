from abc import ABC, abstractmethod

from entities.access_request import AccessRequest


class AuthenticationInterface(ABC):

    @abstractmethod
    def authenticate(self, request: AccessRequest) -> bool:
        pass