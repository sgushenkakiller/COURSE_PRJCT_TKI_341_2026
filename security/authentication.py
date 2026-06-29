from entities.access_request import AccessRequest

from interfaces.access_repository_interface import AccessRepositoryInterface
from interfaces.authentication_interface import AuthenticationInterface


class AuthenticationService(AuthenticationInterface):

    def __init__(
        self,
        repository: AccessRepositoryInterface,
    ) -> None:
        self._repository = repository

    def authenticate(
        self,
        request: AccessRequest,
    ) -> bool:
        card = self._repository.get_card(request.uid)

        if card is None:
            return False

        if not card.active:
            return False

        user = self._repository.get_user(card.owner_id)

        if user is None:
            return False

        if not user.active:
            return False

        if user.blocked:
            return False

        return True