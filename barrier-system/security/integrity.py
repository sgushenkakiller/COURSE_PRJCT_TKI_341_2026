from communication.command_result import CommandResult
from communication.request import Request
from communication.response import Response

from interfaces.crypto_interface import CryptoInterface


class IntegrityService:

    def __init__(
        self,
        crypto: CryptoInterface,
    ) -> None:
        self._crypto = crypto

    def verify_request(
        self,
        request: Request,
        digest: str,
    ) -> bool:
        return self._crypto.verify(
            str(request),
            digest,
        )

    def verify_response(
        self,
        response: Response,
        digest: str,
    ) -> bool:
        return self._crypto.verify(
            str(response),
            digest,
        )

    def verify_command_result(
        self,
        result: CommandResult,
        digest: str,
    ) -> bool:
        return self._crypto.verify(
            str(result),
            digest,
        )

    def calculate_request_digest(
        self,
        request: Request,
    ) -> str:
        return self._crypto.hash(str(request))

    def calculate_response_digest(
        self,
        response: Response,
    ) -> str:
        return self._crypto.hash(str(response))

    def calculate_command_result_digest(
        self,
        result: CommandResult,
    ) -> str:
        return self._crypto.hash(str(result))