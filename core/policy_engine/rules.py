from entities.access_request import AccessRequest
from entities.direction import Direction
from entities.rfid_card import RFIDCard
from entities.user import User


class PolicyRules:

    @staticmethod
    def card_exists(card: RFIDCard | None) -> bool:
        return card is not None

    @staticmethod
    def card_active(card: RFIDCard) -> bool:
        return card.active

    @staticmethod
    def user_exists(user: User | None) -> bool:
        return user is not None

    @staticmethod
    def user_active(user: User) -> bool:
        return user.active

    @staticmethod
    def user_not_blocked(user: User) -> bool:
        return not user.blocked

    @staticmethod
    def access_level(user: User, minimum: int = 1) -> bool:
        return user.access_level >= minimum

    @staticmethod
    def valid_direction(request: AccessRequest) -> bool:
        return request.direction in (Direction.ENTRY, Direction.EXIT)

    @staticmethod
    def valid_reader(request: AccessRequest) -> bool:
        return bool(request.reader_id.strip())
