from devices.operator_panel.display import Display
from devices.operator_panel.keyboard import Keyboard


class OperatorPanel:
    def __init__(
        self,
        display: Display,
        keyboard: Keyboard,
    ) -> None:
        self._display = display
        self._keyboard = keyboard

    @property
    def display(self) -> Display:
        return self._display

    @property
    def keyboard(self) -> Keyboard:
        return self._keyboard

    def show_message(self, message: str) -> None:
        self._display.show(message)

    def clear(self) -> None:
        self._display.clear()

    def read_key(self) -> str | None:
        return self._keyboard.read()