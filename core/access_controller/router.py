from communication.commands import Command

from entities.access_decision import AccessDecision
from entities.policy_result import PolicyResult


class RequestRouter:

    def route(self, decision: AccessDecision) -> Command:

        if decision.result == PolicyResult.ALLOW:
            return Command.OPEN_BARRIER

        return Command.DENY_ACCESS