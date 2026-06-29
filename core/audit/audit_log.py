from entities.audit_record import AuditRecord

from interfaces.access_repository_interface import AccessRepositoryInterface
from interfaces.audit_interface import AuditInterface

from .storage import AuditStorage


class AuditLogger(AuditInterface):

    def __init__(
        self,
        repository: AccessRepositoryInterface
    ) -> None:

        self._storage = AuditStorage(repository)

    def append(
        self,
        record: AuditRecord
    ) -> None:

        self._storage.append(record)

    def records(
        self,
    ) -> list[AuditRecord]:

        return self._storage.get_all()

    def clear(
        self,
    ) -> None:

        self._storage.clear()

    def count(
        self,
    ) -> int:

        return self._storage.count()