from abc import ABC
from abc import abstractmethod

from entities.audit_record import AuditRecord
from entities.rfid_card import RFIDCard
from entities.user import User


class AccessRepositoryInterface(ABC):

    @abstractmethod
    def get_card(
        self,
        uid: str
    ) -> RFIDCard | None:
        ...

    @abstractmethod
    def get_user(
        self,
        identifier: str
    ) -> User | None:
        ...

    @abstractmethod
    def save_record(
        self,
        record: AuditRecord
    ) -> None:
        ...

    @abstractmethod
    def get_records(
        self,
    ) -> list[AuditRecord]:
        ... 