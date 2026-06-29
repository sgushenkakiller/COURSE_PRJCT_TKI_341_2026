class Display:
    def __init__(self) -> None:
        self._text = ""

    @property
    def text(self) -> str:
        return self._text

    def show(self, text: str) -> None:
        self._text = text

    def clear(self) -> None:
        self._text = ""