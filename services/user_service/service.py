from entities.rfid_card import RFIDCard
from entities.user import User

from interfaces.access_repository_interface import AccessRepositoryInterface


class UserService:

    def __init__(
        self,
        repository: AccessRepositoryInterface,
    ) -> None:
        self._repository = repository

    def get_user(self, identifier: str) -> User | None:
        return self._repository.get_user(identifier)

    def get_card(self, uid: str) -> RFIDCard | None:
        return self._repository.get_card(uid)

    def get_records(self):
        return self._repository.get_records()
