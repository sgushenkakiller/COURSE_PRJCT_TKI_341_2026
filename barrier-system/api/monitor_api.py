from communication.response import ResponseMessage
from communication.responses import Response

from entities.audit_record import AuditRecord
from entities.user import User

from interfaces.audit_interface import AuditInterface
from interfaces.authorization_interface import AuthorizationInterface
from interfaces.barrier_interface import BarrierInterface
from interfaces.monitor_interface import MonitorInterface
from interfaces.session_interface import SessionInterface


class MonitorAPI:

    def __init__(
        self,
        monitor: MonitorInterface,
        barrier: BarrierInterface,
        session_service: SessionInterface,
        authorization: AuthorizationInterface,
        audit: AuditInterface,
    ) -> None:
        self._monitor = monitor
        self._barrier = barrier
        self._session_service = session_service
        self._authorization = authorization
        self._audit = audit

    def _check_authorization(self, user: User) -> bool:
        return self._authorization.authorize(user) and user.access_level >= 2

    def get_system_status(self, user: User) -> ResponseMessage:
        try:
            if not self._check_authorization(user):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            barrier_state = self._barrier.state()
            event_count = self._monitor.count()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "barrier_state": barrier_state.value,
                    "event_count": event_count,
                    "status": "operational",
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="MONITOR_API_ERROR",
                    source="MonitorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_barrier_state(self, user: User) -> ResponseMessage:
        try:
            if not self._check_authorization(user):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            state = self._barrier.state()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"barrier_state": state.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="MONITOR_API_ERROR",
                    source="MonitorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_active_sessions(self, user: User) -> ResponseMessage:
        try:
            if not self._check_authorization(user):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            sessions = self._session_service.get_active_sessions()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "active_sessions": [
                        {
                            "session_id": s.session_id,
                            "request_id": s.request_id,
                            "user_id": s.user_id,
                            "barrier_id": s.barrier_id,
                            "opened": s.opened,
                            "started_at": s.started_at.isoformat(),
                        }
                        for s in sessions
                    ]
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="MONITOR_API_ERROR",
                    source="MonitorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_security_events(self, user: User) -> ResponseMessage:
        try:
            if not self._check_authorization(user):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            events = self._monitor.events()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "events": [
                        {
                            "event_type": e.event_type.value,
                            "source": e.source,
                            "description": e.description,
                            "severity": e.severity.value,
                            "timestamp": e.timestamp.isoformat(),
                            "request_id": e.request_id,
                            "user_id": e.user_id,
                            "handled": e.handled,
                        }
                        for e in events
                    ]
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="MONITOR_API_ERROR",
                    source="MonitorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_anomaly_status(self, user: User) -> ResponseMessage:
        try:
            if not self._check_authorization(user):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            events = self._monitor.events()

            anomalies = [
                e for e in events
                if not e.handled
            ]

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "total_events": len(events),
                    "unhandled_events": len(anomalies),
                    "anomaly_detection_active": True,
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="MONITOR_API_ERROR",
                    source="MonitorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def health_check(self) -> ResponseMessage:
        try:
            barrier_state = self._barrier.state()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "healthy": True,
                    "barrier_state": barrier_state.value,
                },
            )

        except Exception as exc:
            return ResponseMessage(
                status=Response.DEVICE_ERROR,
                payload={"healthy": False, "error": str(exc)},
            )
