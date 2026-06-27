from entities.access_decision import AccessDecision
from entities.access_request import AccessRequest

from interfaces.access_repository_interface import AccessRepositoryInterface
from interfaces.policy_interface import PolicyInterface

from .decision import DecisionFactory
from .rules import PolicyRules


class PolicyEngine(PolicyInterface):

    def __init__(
        self,
        repository: AccessRepositoryInterface
    ) -> None:

        self._repository = repository

    def evaluate(
        self,
        request: AccessRequest
    ) -> AccessDecision:

        if not PolicyRules.valid_reader(request):
            return DecisionFactory.deny(
                request.request_id,
                "Invalid reader"
            )

        if not PolicyRules.valid_direction(request):
            return DecisionFactory.deny(
                request.request_id,
                "Invalid direction"
            )

        card = self._repository.get_card(request.uid)

        if not PolicyRules.card_exists(card):
            return DecisionFactory.deny(
                request.request_id,
                "Card not found"
            )

        if not PolicyRules.card_active(card):
            return DecisionFactory.deny(
                request.request_id,
                "Card disabled"
            )

        user = self._repository.get_user(card.owner_id)

        if not PolicyRules.user_exists(user):
            return DecisionFactory.deny(
                request.request_id,
                "Unknown user"
            )

        if not PolicyRules.user_active(user):
            return DecisionFactory.deny(
                request.request_id,
                "Inactive user"
            )

        if not PolicyRules.user_not_blocked(user):
            return DecisionFactory.deny(
                request.request_id,
                "Blocked user"
            )

        if not PolicyRules.access_level(user):
            return DecisionFactory.deny(
                request.request_id,
                "Insufficient privileges"
            )

        return DecisionFactory.allow(request.request_id)