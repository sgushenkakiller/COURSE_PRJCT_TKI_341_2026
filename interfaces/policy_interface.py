from abc import ABC, abstractmethod

from entities.access_decision import AccessDecision
from entities.access_request import AccessRequest


class PolicyInterface(ABC):

    @abstractmethod
    def evaluate(self, request: AccessRequest) -> AccessDecision:
        pass
