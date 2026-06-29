import hashlib
import hmac

from interfaces.crypto_interface import CryptoInterface


class CryptoService(CryptoInterface):

    def __init__(self, algorithm: str = "sha256") -> None:
        self._algorithm = algorithm

    def hash(self, data: str) -> str:
        return hashlib.new(
            self._algorithm,
            data.encode("utf-8"),
        ).hexdigest()

    def verify(
        self,
        data: str,
        digest: str,
    ) -> bool:
        calculated = self.hash(data)
        return hmac.compare_digest(calculated, digest)