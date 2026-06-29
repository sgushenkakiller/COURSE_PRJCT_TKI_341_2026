from entities.audit_record import AuditRecord
from entities.rfid_card import RFIDCard
from entities.user import User

from interfaces.access_repository_interface import AccessRepositoryInterface

from .models import DatabaseModel


class AccessRepository(AccessRepositoryInterface):

    def __init__(self) -> None:
        self._database = DatabaseModel()

    def get_card(
        self,
        uid: str
    ) -> RFIDCard | None:

        return self._database.cards.get(uid)

    def get_user(
        self,
        identifier: str
    ) -> User | None:

        return self._database.users.get(identifier)

    def save_record(
        self,
        record: AuditRecord
    ) -> None:

        self._database.audit.append(record)

    def get_records(self) -> list[AuditRecord]:

        return list(self._database.audit)

    def add_user(
        self,
        user: User
    ) -> None:

        self._database.users[user.identifier] = user

    def add_card(
        self,
        card: RFIDCard
    ) -> None:

        self._database.cards[card.uid] = card

    def remove_user(
        self,
        identifier: str
    ) -> None:

        self._database.users.pop(identifier, None)

    def remove_card(
        self,
        uid: str
    ) -> None:

        self._database.cards.pop(uid, None)

    def get_users(self) -> list[User]:

        return list(self._database.users.values())

    def get_cards(self) -> list[RFIDCard]:

        return list(self._database.cards.values())

    def clear_audit(self) -> None:

        self._database.audit.clear()