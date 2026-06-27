from entities.user import User

from interfaces.authorization_interface import AuthorizationInterface


class AuthorizationService(AuthorizationInterface):

    def authorize(
        self,
        user: User,
    ) -> bool:
        if not user.active:
            return False

        if user.blocked:
            return False

        return user.access_level > 0