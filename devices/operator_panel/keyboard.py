from typing import Optional


class Keyboard:
    def __init__(self) -> None:
        self._last_key: Optional[str] = None

    @property
    def last_key(self) -> Optional[str]:
        return self._last_key

    def press(self, key: str) -> None:
        self._last_key = key

    def read(self) -> Optional[str]:
        key = self._last_key
        self._last_key = None
        return key