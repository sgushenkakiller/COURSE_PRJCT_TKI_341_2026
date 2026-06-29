from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RFIDCard:
    """
    RFID-карта пользователя.
    """

    uid: str

    owner_id: str

    issue_date: str

    expiration_date: str

    active: bool = True