from entities.administrator import Administrator
from entities.audit_record import AuditRecord
from entities.rfid_card import RFIDCard
from entities.security_event import SecurityEvent
from entities.security_event_type import SecurityEventType
from entities.severity import Severity
from entities.user import User

from interfaces.access_repository_interface import AccessRepositoryInterface
from interfaces.audit_interface import AuditInterface
from interfaces.monitor_interface import MonitorInterface


class AdministrationService:

    def __init__(
        self,
        repository: AccessRepositoryInterface,
        audit: AuditInterface,
        monitor: MonitorInterface,
    ) -> None:
        self._repository = repository
        self._audit = audit
        self._monitor = monitor

    def add_user(self, user: User, admin_id: str) -> None:
        self._repository.add_user(user)

        self._audit.append(
            AuditRecord(
                event="USER_ADDED",
                source=admin_id,
                details=f"User {user.identifier} added",
            )
        )

    def remove_user(self, identifier: str, admin_id: str) -> None:
        self._repository.remove_user(identifier)

        self._audit.append(
            AuditRecord(
                event="USER_REMOVED",
                source=admin_id,
                details=f"User {identifier} removed",
            )
        )

    def block_user(self, identifier: str, admin_id: str) -> bool:
        user = self._repository.get_user(identifier)

        if user is None:
            return False

        user.blocked = True

        self._audit.append(
            AuditRecord(
                event="USER_BLOCKED",
                source=admin_id,
                details=f"User {identifier} blocked",
            )
        )

        self._monitor.notify(
            SecurityEvent(
                event_type=SecurityEventType.BLOCKED_USER,
                source=admin_id,
                description=f"User {identifier} was blocked by administrator",
                severity=Severity.HIGH,
                user_id=identifier,
            )
        )

        return True

    def unblock_user(self, identifier: str, admin_id: str) -> bool:
        user = self._repository.get_user(identifier)

        if user is None:
            return False

        user.blocked = False

        self._audit.append(
            AuditRecord(
                event="USER_UNBLOCKED",
                source=admin_id,
                details=f"User {identifier} unblocked",
            )
        )

        return True

    def register_card(self, card: RFIDCard, admin_id: str) -> None:
        self._repository.add_card(card)

        self._audit.append(
            AuditRecord(
                event="CARD_REGISTERED",
                source=admin_id,
                details=f"Card {card.uid} registered for user {card.owner_id}",
            )
        )

    def revoke_card(self, uid: str, admin_id: str) -> bool:
        card = self._repository.get_card(uid)

        if card is None:
            return False

        self._repository.remove_card(uid)

        self._audit.append(
            AuditRecord(
                event="CARD_REVOKED",
                source=admin_id,
                details=f"Card {uid} revoked",
            )
        )

        return True

    def get_all_users(self) -> list[User]:
        return self._repository.get_users()

    def get_all_cards(self) -> list[RFIDCard]:
        return self._repository.get_cards()

    def get_audit_log(self) -> list[AuditRecord]:
        return self._repository.get_records()

    def clear_audit_log(self, admin_id: str) -> None:
        self._repository.clear_audit()

        self._audit.append(
            AuditRecord(
                event="AUDIT_CLEARED",
                source=admin_id,
                details="Audit log cleared by administrator",
            )
        )
