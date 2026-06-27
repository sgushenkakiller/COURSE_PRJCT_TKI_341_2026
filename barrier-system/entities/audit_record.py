from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class AuditRecord:
    """
    Запись журнала аудита.
    """

    event: str

    source: str

    details: str

    timestamp: datetime = field(default_factory=datetime.utcnow)