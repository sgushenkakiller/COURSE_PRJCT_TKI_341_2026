from dataclasses import dataclass, field
from datetime import datetime

from entities.direction import Direction


@dataclass(slots=True, frozen=True)
class AccessRequest:

    request_id: str

    uid: str

    reader_id: str

    direction: Direction = Direction.ENTRY

    timestamp: datetime = field(default_factory=datetime.utcnow)

    vehicle_number: str | None = None

    source_ip: str | None = None