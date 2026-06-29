from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class AccessSession:
    """
    Сессия прохода через КПП.
    """

    session_id: str

    request_id: str

    user_id: str

    barrier_id: str

    opened: bool = False

    started_at: datetime = field(default_factory=datetime.utcnow)

    finished_at: datetime | None = None