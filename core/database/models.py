from dataclasses import dataclass, field

from entities.rfid_card import RFIDCard
from entities.user import User
from entities.audit_record import AuditRecord


@dataclass(slots=True)
class DatabaseModel:

    users: dict[str, User] = field(default_factory=dict)

    cards: dict[str, RFIDCard] = field(default_factory=dict)

    audit: list[AuditRecord] = field(default_factory=list)