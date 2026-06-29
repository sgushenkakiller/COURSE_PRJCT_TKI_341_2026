from interfaces.access_controller_interface import AccessControllerInterface
from interfaces.audit_interface import AuditInterface
from interfaces.barrier_interface import BarrierInterface
from interfaces.monitor_interface import MonitorInterface
from interfaces.policy_interface import PolicyInterface

from communication.commands import Command

from entities.access_decision import AccessDecision
from entities.access_request import AccessRequest
from entities.audit_record import AuditRecord
from entities.security_event import SecurityEvent
from entities.security_event_type import SecurityEventType
from entities.severity import Severity

from .router import RequestRouter
from .validator import RequestValidator


class AccessController(AccessControllerInterface):

    def __init__(
        self,
        policy: PolicyInterface,
        barrier: BarrierInterface,
        monitor: MonitorInterface,
        audit: AuditInterface,
    ) -> None:

        self._policy = policy
        self._barrier = barrier
        self._monitor = monitor
        self._audit = audit

        self._validator = RequestValidator()
        self._router = RequestRouter()

    def process_request(
        self,
        request: AccessRequest
    ) -> AccessDecision:

        if not self._validator.validate(request):

            event = SecurityEvent(
                event_type=SecurityEventType.POLICY_VIOLATION,
                source="AccessController",
                description="Invalid access request",
                severity=Severity.HIGH,
                request_id=request.request_id,
            )

            self._monitor.notify(event)

            self._audit.append(
                AuditRecord(
                    event="INVALID_REQUEST",
                    source="AccessController",
                    details="Validation failed",
                )
            )

            return self._policy.evaluate(request)

        decision = self._policy.evaluate(request)

        command = self._router.route(decision)

        self._barrier.execute(command)

        event_type = (
            SecurityEventType.ACCESS_GRANTED
            if command == Command.OPEN_BARRIER
            else SecurityEventType.ACCESS_DENIED
        )

        severity = (
            Severity.LOW
            if command == Command.OPEN_BARRIER
            else Severity.MEDIUM
        )

        self._monitor.notify(
            SecurityEvent(
                event_type=event_type,
                source="AccessController",
                description=decision.reason,
                severity=severity,
                request_id=request.request_id,
            )
        )

        self._audit.append(
            AuditRecord(
                event=decision.result.value,
                source="AccessController",
                details=decision.reason,
            )
        )

        return decision