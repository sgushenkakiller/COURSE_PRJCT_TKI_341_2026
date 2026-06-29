from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from communication.protocol import Protocol


@dataclass(slots=True)
class Request:

    identifier: str = field(default_factory=lambda: str(uuid4()))

    sender: str = ""

    receiver: str = ""

    protocol: Protocol = Protocol.INTERNAL

    payload: dict = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)