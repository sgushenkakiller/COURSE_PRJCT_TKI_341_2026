from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """
    Пользователь системы.
    """

    identifier: str

    full_name: str

    access_level: int

    department: str

    blocked: bool = False

    active: bool = True