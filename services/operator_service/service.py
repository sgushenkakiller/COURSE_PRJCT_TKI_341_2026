from communication.commands import Command
from communication.command_result import CommandResult

from entities.audit_record import AuditRecord
from entities.barrier_state import BarrierState
from entities.security_event import SecurityEvent
from entities.security_event_type import SecurityEventType
from entities.severity import Severity

from interfaces.access_repository_interface import AccessRepositoryInterface
from interfaces.audit_interface import AuditInterface
from interfaces.barrier_interface import BarrierInterface
from interfaces.monitor_interface import MonitorInterface


class OperatorService:

    def __init__(
        self,
        barrier: BarrierInterface,
        repository: AccessRepositoryInterface,
        audit: AuditInterface,
        monitor: MonitorInterface,
    ) -> None:
        self._barrier = barrier
        self._repository = repository
        self._audit = audit
        self._monitor = monitor

    def manual_open(self, operator_id: str) -> CommandResult:
        result = self._barrier.execute(Command.OPEN_BARRIER)

        self._audit.append(AuditRecord(
            event="OPERATOR_OPEN",
            source=operator_id,
            details="Barrier opened by operator",
        ))

        self._monitor.notify(SecurityEvent(
            event_type=SecurityEventType.BARRIER_OPENED,
            source=operator_id,
            description="Barrier opened by operator panel command",
            severity=Severity.MEDIUM,
        ))

        return result

    def manual_close(self, operator_id: str) -> CommandResult:
        result = self._barrier.execute(Command.CLOSE_BARRIER)

        self._audit.append(AuditRecord(
            event="OPERATOR_CLOSE",
            source=operator_id,
            details="Barrier closed by operator",
        ))

        self._monitor.notify(SecurityEvent(
            event_type=SecurityEventType.BARRIER_CLOSED,
            source=operator_id,
            description="Barrier closed by operator panel command",
            severity=Severity.LOW,
        ))

        return result

    def barrier_state(self) -> BarrierState:
        return self._barrier.state()

    def get_access_history(self) -> list:
        return self._repository.get_records()
