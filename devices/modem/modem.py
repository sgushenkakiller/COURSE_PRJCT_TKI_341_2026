from typing import List

from devices.modem.message import ModemMessage


class Modem:
    def __init__(self) -> None:
        self._connected = False
        self._outbox: List[ModemMessage] = []

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def outbox(self) -> tuple[ModemMessage, ...]:
        return tuple(self._outbox)

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def send(self, message: ModemMessage) -> bool:
        if not self._connected:
            return False

        self._outbox.append(message)
        return True

    def clear_outbox(self) -> None:
        self._outbox.clear()