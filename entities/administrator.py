from dataclasses import dataclass

from .user import User


@dataclass(slots=True)
class Administrator(User):
    superuser: bool = True
    can_modify_policy: bool = True
    can_manage_users: bool = True
