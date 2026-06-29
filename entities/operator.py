from dataclasses import dataclass

from .user import User


@dataclass(slots=True)
class Operator(User):
    console_id: str = ""
    shift: str = ""
    can_override: bool = False
