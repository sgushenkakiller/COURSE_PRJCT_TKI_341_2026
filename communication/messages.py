from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from communication.commands import Command
from communication.protocol import Protocol
from communication.responses import Response


@dataclass(slots=True)
class Message:

    identifier: str = field(default_factory=lambda: str(uuid4()))

    sender: str = ""

    receiver: str = ""

    protocol: Protocol = Protocol.INTERNAL

    command: Command | None = None

    response: Response | None = None

    payload: dict = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)