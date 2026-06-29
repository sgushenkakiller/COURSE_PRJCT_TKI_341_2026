from typing import Optional

from entities.reader_state import ReaderState


class RFIDScanner:
    def __init__(self) -> None:
        self._state = ReaderState.READY

    @property
    def state(self) -> ReaderState:
        return self._state

    def enable(self) -> None:
        self._state = ReaderState.READY

    def disable(self) -> None:
        self._state = ReaderState.DISABLED

    def read_uid(self) -> Optional[str]:
        if self._state != ReaderState.READY:
            return None

        return None