from uuid import uuid4

from communication.commands import Command
from communication.command_result import CommandResult

from entities.access_decision import AccessDecision
from entities.access_request import AccessRequest
from entities.audit_record import AuditRecord
from entities.barrier_state import BarrierState
from entities.direction import Direction
from entities.policy_result import PolicyResult
from entities.security_event import SecurityEvent
from entities.security_event_type import SecurityEventType
from entities.severity import Severity

from interfaces.access_controller_interface import AccessControllerInterface
from interfaces.audit_interface import AuditInterface
from interfaces.barrier_interface import BarrierInterface
from interfaces.monitor_interface import MonitorInterface


class AccessService:

    def __init__(
        self,
        controller: AccessControllerInterface,
        barrier: BarrierInterface,
        monitor: MonitorInterface,
        audit: AuditInterface,
    ) -> None:
        self._controller = controller
        self._barrier = barrier
        self._monitor = monitor
        self._audit = audit

    def request_access(
        self,
        uid: str,
        reader_id: str,
        direction: Direction = Direction.ENTRY,
    ) -> AccessDecision:
        request = AccessRequest(
            request_id=str(uuid4()),
            uid=uid,
            reader_id=reader_id,
            direction=direction,
        )
        return self._controller.process_request(request)

    def open_barrier(self, caller_id: str) -> CommandResult:
        result = self._barrier.execute(Command.OPEN_BARRIER)

        self._audit.append(AuditRecord(
            event="MANUAL_OPEN",
            source=caller_id,
            details="Manual barrier open command issued",
        ))

        self._monitor.notify(SecurityEvent(
            event_type=SecurityEventType.BARRIER_OPENED,
            source=caller_id,
            description="Barrier opened manually",
            severity=Severity.MEDIUM,
        ))

        return result

    def close_barrier(self, caller_id: str) -> CommandResult:
        result = self._barrier.execute(Command.CLOSE_BARRIER)

        self._audit.append(AuditRecord(
            event="MANUAL_CLOSE",
            source=caller_id,
            details="Manual barrier close command issued",
        ))

        self._monitor.notify(SecurityEvent(
            event_type=SecurityEventType.BARRIER_CLOSED,
            source=caller_id,
            description="Barrier closed manually",
            severity=Severity.LOW,
        ))

        return result

    def barrier_state(self) -> BarrierState:
        return self._barrier.state()
