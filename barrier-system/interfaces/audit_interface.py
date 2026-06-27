from abc import ABC
from abc import abstractmethod

from entities.audit_record import AuditRecord


class AuditInterface(ABC):

    @abstractmethod
    def append(self, record: AuditRecord) -> None:
        ...