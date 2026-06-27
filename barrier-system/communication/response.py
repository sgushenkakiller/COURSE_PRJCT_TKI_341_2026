from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from communication.responses import Response


@dataclass(slots=True)
class ResponseMessage:

    identifier: str = field(default_factory=lambda: str(uuid4()))

    status: Response = Response.SUCCESS

    payload: dict = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)