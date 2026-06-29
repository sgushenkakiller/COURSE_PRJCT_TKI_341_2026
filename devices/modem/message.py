from dataclasses import dataclass


@dataclass(frozen=True)
class ModemMessage:
    recipient: str
    subject: str
    body: str