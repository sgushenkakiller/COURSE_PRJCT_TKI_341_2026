from communication.response import ResponseMessage
from communication.responses import Response

from entities.audit_record import AuditRecord
from entities.rfid_card import RFIDCard
from entities.user import User

from interfaces.audit_interface import AuditInterface
from interfaces.authorization_interface import AuthorizationInterface

from services.administration_service import AdministrationService


class AdminAPI:

    def __init__(
        self,
        administration_service: AdministrationService,
        authorization: AuthorizationInterface,
        audit: AuditInterface,
    ) -> None:
        self._administration_service = administration_service
        self._authorization = authorization
        self._audit = audit

    def _check_authorization(self, admin: User) -> bool:
        return self._authorization.authorize(admin) and admin.access_level >= 3

    def add_user(self, admin: User, user: User) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details=f"Unauthorized attempt to add user {user.identifier}",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            self._administration_service.add_user(user, admin.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"user_id": user.identifier},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def remove_user(self, admin: User, identifier: str) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details=f"Unauthorized attempt to remove user {identifier}",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            self._administration_service.remove_user(identifier, admin.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"user_id": identifier},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def block_user(self, admin: User, identifier: str) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details=f"Unauthorized attempt to block user {identifier}",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            success = self._administration_service.block_user(identifier, admin.identifier)

            if not success:
                return ResponseMessage(
                    status=Response.FAILURE,
                    payload={"error": f"User {identifier} not found"},
                )

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"user_id": identifier, "blocked": True},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def unblock_user(self, admin: User, identifier: str) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details=f"Unauthorized attempt to unblock user {identifier}",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            success = self._administration_service.unblock_user(identifier, admin.identifier)

            if not success:
                return ResponseMessage(
                    status=Response.FAILURE,
                    payload={"error": f"User {identifier} not found"},
                )

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"user_id": identifier, "blocked": False},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def register_card(self, admin: User, card: RFIDCard) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details=f"Unauthorized attempt to register card {card.uid}",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            self._administration_service.register_card(card, admin.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"card_uid": card.uid, "owner_id": card.owner_id},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def revoke_card(self, admin: User, uid: str) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details=f"Unauthorized attempt to revoke card {uid}",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            success = self._administration_service.revoke_card(uid, admin.identifier)

            if not success:
                return ResponseMessage(
                    status=Response.FAILURE,
                    payload={"error": f"Card {uid} not found"},
                )

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"card_uid": uid, "revoked": True},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def list_users(self, admin: User) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            users = self._administration_service.get_all_users()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "users": [
                        {
                            "identifier": u.identifier,
                            "full_name": u.full_name,
                            "access_level": u.access_level,
                            "department": u.department,
                            "blocked": u.blocked,
                            "active": u.active,
                        }
                        for u in users
                    ]
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def list_cards(self, admin: User) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            cards = self._administration_service.get_all_cards()

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={
                    "cards": [
                        {
                            "uid": c.uid,
                            "owner_id": c.owner_id,
                            "issue_date": c.issue_date,
                            "expiration_date": c.expiration_date,
                            "active": c.active,
                        }
                        for c in cards
                    ]
                },
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def get_audit_log(self, admin: User) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            records = self._administration_service.get_audit_log()

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
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def clear_audit_log(self, admin: User) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            self._administration_service.clear_audit_log(admin.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"cleared": True},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def emergency_open(self, admin: User, access_service) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details="Unauthorized emergency open attempt",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            result = access_service.open_barrier(admin.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"command_result": result.value, "emergency": True},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )

    def emergency_close(self, admin: User, access_service) -> ResponseMessage:
        try:
            if not self._check_authorization(admin):
                self._audit.append(
                    AuditRecord(
                        event="UNAUTHORIZED_ATTEMPT",
                        source=admin.identifier,
                        details="Unauthorized emergency close attempt",
                    )
                )

                return ResponseMessage(
                    status=Response.UNAUTHORIZED,
                    payload={"error": "Insufficient privileges"},
                )

            result = access_service.close_barrier(admin.identifier)

            return ResponseMessage(
                status=Response.SUCCESS,
                payload={"command_result": result.value, "emergency": True},
            )

        except Exception as exc:
            self._audit.append(
                AuditRecord(
                    event="ADMIN_API_ERROR",
                    source="AdminAPI",
                    details=str(exc),
                )
            )

            return ResponseMessage(
                status=Response.FAILURE,
                payload={"error": str(exc)},
            )
