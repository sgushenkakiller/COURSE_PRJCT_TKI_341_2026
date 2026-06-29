from interfaces.access_repository_interface import AccessRepositoryInterface

from entities.audit_record import AuditRecord


class AuditStorage:

    def __init__(
        self,
        repository: AccessRepositoryInterface
    ) -> None:

        self._repository = repository

    def append(
        self,
        record: AuditRecord
    ) -> None:

        self._repository.save_record(record)

    def get_all(self) -> list[AuditRecord]:

        return self._repository.get_records()

    def clear(self) -> None:

        records = self._repository.get_records()

        records.clear()

    def count(self) -> int:

        return len(self._repository.get_records())