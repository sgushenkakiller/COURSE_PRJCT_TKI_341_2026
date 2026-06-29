from datetime import datetime

from entities.access_session import AccessSession
from interfaces.session_interface import SessionInterface


class SessionService(SessionInterface):

    def __init__(self) -> None:
        self._sessions: dict[str, AccessSession] = {}

    def create(self, session: AccessSession) -> None:
        self._sessions[session.session_id] = session

    def close(self, session_id: str) -> None:
        session = self._sessions.get(session_id)

        if session is None:
            return

        session.finished_at = datetime.utcnow()

    def get(self, session_id: str) -> AccessSession | None:
        return self._sessions.get(session_id)

    def exists(self, session_id: str) -> bool:
        return session_id in self._sessions

    def is_active(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)

        if session is None:
            return False

        return session.finished_at is None

    def remove(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def clear(self) -> None:
        self._sessions.clear()

    def get_active_sessions(self) -> list[AccessSession]:
        return [
            session
            for session in self._sessions.values()
            if session.finished_at is None
        ]