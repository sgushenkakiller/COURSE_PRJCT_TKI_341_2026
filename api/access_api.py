from communication.response import ResponseMessage
from communication.responses import Response

from entities.audit_record import AuditRecord
from entities.direction import Direction
from entities.policy_result import PolicyResult

from interfaces.audit_interface import AuditInterface
from interfaces.authentication_interface import AuthenticationInterface

from services.access_service import AccessService


class AccessAPI:

    def __init__(
        self,
        access_service: AccessService,
        authentication: AuthenticationInterface,
        audit: AuditInterface,
    ) -> None:
        self._access_service = access_service
        self._authentication = authentication
        self._audit = audit

    def process_card_read(
        self,
        uid: str,
        reader_id: str,
        direction: str = "entry",
    ) -> ResponseMessage:
        try:
            dir_value = Direction.ENTRY if direction == "entry" else Direction.EXIT

            decision = self._access_service.request_access(
                uid=uid,
                reader_id=reader_id,
                direction=dir_value,
            )

            granted = decision.result == PolicyResult.ALLOW

            status = Response.ACCEPTED if granted else Response.REJECTED

            return ResponseMessage(
                status=status,
                payload={
                    "request_id": decision.request_id,
                    "result": decision.result.value,
                    "reason": decision.reason,
                    "operator_required": decision.operator_required,
                    "administrator_required": decision.administrator_required,
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ACCESS_API_ERROR",
                    source="AccessAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_barrier_state(self) -> ResponseMessage:
        try:
            state = self._access_service.barrier_state()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"barrier_state": state.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ACCESS_API_ERROR",
                    source="AccessAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def open_barrier(self, caller_id: str) -> ResponseMessage:
        try:
            result = self._access_service.open_barrier(caller_id)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"command_result": result.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ACCESS_API_ERROR",
                    source="AccessAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def close_barrier(self, caller_id: str) -> ResponseMessage:
        try:
            result = self._access_service.close_barrier(caller_id)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"command_result": result.value},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ACCESS_API_ERROR",
                    source="AccessAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )
