from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class Event:

    identifier: str = field(default_factory=lambda: str(uuid4()))

    source: str = ""

    name: str = ""

    payload: dict = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)