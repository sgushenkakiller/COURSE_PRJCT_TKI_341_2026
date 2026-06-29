from entities.access_decision import AccessDecision
from entities.policy_result import PolicyResult


class DecisionFactory:

    @staticmethod
    def allow(request_id: str) -> AccessDecision:
        return AccessDecision(
            request_id=request_id,
            result=PolicyResult.ALLOW,
            reason="Access granted"
        )

    @staticmethod
    def deny(request_id: str, reason: str) -> AccessDecision:
        return AccessDecision(
            request_id=request_id,
            result=PolicyResult.DENY,
            reason=reason
        )

    @staticmethod
    def operator(request_id: str, reason: str) -> AccessDecision:
        return AccessDecision(
            request_id=request_id,
            result=PolicyResult.REQUIRE_OPERATOR,
            reason=reason,
            operator_required=True
        )

    @staticmethod
    def administrator(request_id: str, reason: str) -> AccessDecision:
        return AccessDecision(
            request_id=request_id,
            result=PolicyResult.REQUIRE_ADMINISTRATOR,
            reason=reason,
            administrator_required=True
        )