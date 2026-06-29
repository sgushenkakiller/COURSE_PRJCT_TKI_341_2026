from entities.security_event import SecurityEvent


class EventHandler:

    def __init__(self) -> None:
        self._events: list[SecurityEvent] = []

    def handle(
        self,
        event: SecurityEvent
    ) -> None:

        event.handled = True
        self._events.append(event)

    def events(self) -> list[SecurityEvent]:

        return list(self._events)

    def clear(self) -> None:

        self._events.clear()

    def count(self) -> int:

        return len(self._events)