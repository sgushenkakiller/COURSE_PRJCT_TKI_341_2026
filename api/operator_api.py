from communication.response import ResponseMessage
from communication.responses import Response

from entities.audit_record import AuditRecord
from entities.operator import Operator

from interfaces.audit_interface import AuditInterface
from interfaces.authorization_interface import AuthorizationInterface
from interfaces.barrier_interface import BarrierInterface

from services.operator_service import OperatorService


class OperatorAPI:

    def __init__(
        self,
        operator_service: OperatorService,
        barrier: BarrierInterface,
        authorization: AuthorizationInterface,
        audit: AuditInterface,
    ) -> None:
        self._operator_service = operator_service
        self._barrier = barrier
        self._authorization = authorization
        self._audit = audit

    def _check_authorization(self, operator: Operator) -> bool:
        return self._authorization.authorize(operator) and operator.access_level >= 2

    def authenticate_operator(self, operator: Operator) -> ResponseMessage:
        try:
            authorized = self._check_authorization(operator)

            if not authorized:
                self._audit.append(
                    AuditRecord(
                        event="OPERATOR_AUTH_FAILED",
                        source=operator.identifier,
                        details="Operator authentication failed",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"authenticated": False},
                )

            self._audit.append(
                AuditRecord(
                    event="OPERATOR_LOGIN",
                    source=operator.identifier,
                    details=f"Operator {operator.identifier} authenticated on console {operator.console_id}",
                )
            )

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "authenticated": True,
                    "operator_id": operator.identifier,
                    "console_id": operator.console_id,
                    "can_override": operator.can_override,
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="OPERATOR_API_ERROR",
                    source="OperatorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def open_barrier(self, operator: Operator) -> ResponseMessage:
        try:
            if not self._check_authorization(operator):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=operator.identifier,
                        details="Unauthorized barrier open attempt by operator",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            result = self._operator_service.manual_open(operator.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"command_result": result.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="OPERATOR_API_ERROR",
                    source="OperatorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def close_barrier(self, operator: Operator) -> ResponseMessage:
        try:
            if not self._check_authorization(operator):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=operator.identifier,
                        details="Unauthorized barrier close attempt by operator",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            result = self._operator_service.manual_close(operator.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"command_result": result.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="OPERATOR_API_ERROR",
                    source="OperatorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_barrier_state(self, operator: Operator) -> ResponseMessage:
        try:
            if not self._check_authorization(operator):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            state = self._operator_service.barrier_state()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"barrier_state": state.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="OPERATOR_API_ERROR",
                    source="OperatorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_access_history(self, operator: Operator) -> ResponseMessage:
        try:
            if not self._check_authorization(operator):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            records = self._operator_service.get_access_history()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "records": [
                        {
                            "event": r.event,
                            "source": r.source,
                            "details": r.details,
                            "timestamp": r.timestamp.isoformat(),
                        }
                        for r in records
                    ]
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="OPERATOR_API_ERROR",
                    source="OperatorAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )
