from collections import deque

from communication.messages import Message


class CommunicationChannel:

    def __init__(self) -> None:
        self._queue = deque()

    def send(self, message: Message) -> None:
        self._queue.append(message)

    def receive(self) -> Message | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)