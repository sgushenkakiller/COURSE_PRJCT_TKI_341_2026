from abc import ABC
from abc import abstractmethod

from entities.access_decision import AccessDecision
from entities.access_request import AccessRequest


class AccessControllerInterface(ABC):

    @abstractmethod
    def process_request(
        self,
        request: AccessRequest
    ) -> AccessDecision:
        ...