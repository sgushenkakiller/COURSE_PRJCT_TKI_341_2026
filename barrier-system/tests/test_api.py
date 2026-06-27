import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from api.access_api import AccessAPI
from api.admin_api import AdminAPI
from api.monitor_api import MonitorAPI
from api.operator_api import OperatorAPI
from communication.responses import Response
from entities.access_decision import AccessDecision
from entities.administrator import Administrator
from entities.audit_record import AuditRecord
from entities.barrier_state import BarrierState
from entities.operator import Operator
from entities.policy_result import PolicyResult
from entities.rfid_card import RFIDCard
from entities.user import User


def make_admin() -> Administrator:
    return Administrator(
        identifier="admin-001",
        full_name="Admin",
        access_level=3,
        department="IT",
    )


def make_operator() -> Operator:
    return Operator(
        identifier="op-001",
        full_name="Operator",
        access_level=2,
        department="Security",
        console_id="console-01",
        shift="day",
    )


def make_user(access_level: int = 1) -> User:
    return User(
        identifier="user-001",
        full_name="User",
        access_level=access_level,
        department="Dev",
    )


def make_decision(result: PolicyResult = PolicyResult.ALLOW) -> AccessDecision:
    return AccessDecision(
        request_id=str(uuid4()),
        result=result,
        reason="Test",
    )


class TestAccessAPI:
    def setup_method(self):
        self.access_service = MagicMock()
        self.authentication = MagicMock()
        self.audit = MagicMock()
        self.api = AccessAPI(self.access_service, self.authentication, self.audit)

    def test_card_read_allowed(self):
        self.access_service.request_access.return_value = make_decision(PolicyResult.ALLOW)
        self.access_service.barrier_state.return_value = BarrierState.OPEN
        resp = self.api.process_card_read("CARD-001", "reader-01", "entry")
        assert resp.status == Response.ACCEPTED

    def test_card_read_denied(self):
        self.access_service.request_access.return_value = make_decision(PolicyResult.DENY)
        self.access_service.barrier_state.return_value = BarrierState.CLOSED
        resp = self.api.process_card_read("CARD-999", "reader-01", "entry")
        assert resp.status == Response.REJECTED

    def test_get_barrier_state(self):
        self.access_service.barrier_state.return_value = BarrierState.CLOSED
        resp = self.api.get_barrier_state()
        assert resp.status == Response.SUCCESS
        assert resp.payload["barrier_state"] == "closed"

    def test_open_barrier(self):
        from communication.command_result import CommandResult
        self.access_service.open_barrier.return_value = CommandResult.SUCCESS
        resp = self.api.open_barrier("caller-001")
        assert resp.status == Response.SUCCESS

    def test_close_barrier(self):
        from communication.command_result import CommandResult
        self.access_service.close_barrier.return_value = CommandResult.SUCCESS
        resp = self.api.close_barrier("caller-001")
        assert resp.status == Response.SUCCESS


class TestAdminAPI:
    def setup_method(self):
        self.admin_service = MagicMock()
        self.authorization = MagicMock()
        self.authorization.authorize.return_value = True
        self.audit = MagicMock()
        self.api = AdminAPI(self.admin_service, self.authorization, self.audit)

    def test_add_user_authorized(self):
        admin = make_admin()
        new_user = make_user()
        resp = self.api.add_user(admin, new_user)
        assert resp.status == Response.SUCCESS

    def test_add_user_unauthorized(self):
        low_user = make_user(access_level=1)
        new_user = make_user()
        resp = self.api.add_user(low_user, new_user)
        assert resp.status == Response.UNAUTHORIZED

    def test_block_user_not_found(self):
        admin = make_admin()
        self.admin_service.block_user.return_value = False
        resp = self.api.block_user(admin, "nonexistent")
        assert resp.status == Response.FAILURE

    def test_revoke_card_not_found(self):
        admin = make_admin()
        self.admin_service.revoke_card.return_value = False
        resp = self.api.revoke_card(admin, "BAD-UID")
        assert resp.status == Response.FAILURE

    def test_get_audit_log(self):
        admin = make_admin()
        self.admin_service.get_audit_log.return_value = [
            AuditRecord(event="TEST", source="sys", details="d")
        ]
        resp = self.api.get_audit_log(admin)
        assert resp.status == Response.SUCCESS
        assert len(resp.payload["records"]) == 1


class TestMonitorAPI:
    def setup_method(self):
        self.monitor = MagicMock()
        self.barrier = MagicMock()
        self.session_service = MagicMock()
        self.authorization = MagicMock()
        self.authorization.authorize.return_value = True
        self.audit = MagicMock()
        self.api = MonitorAPI(
            self.monitor, self.barrier, self.session_service,
            self.authorization, self.audit
        )

    def test_get_barrier_state_authorized(self):
        user = make_user(access_level=2)
        self.barrier.state.return_value = BarrierState.CLOSED
        resp = self.api.get_barrier_state(user)
        assert resp.status == Response.SUCCESS

    def test_get_barrier_state_unauthorized(self):
        user = make_user(access_level=1)
        resp = self.api.get_barrier_state(user)
        assert resp.status == Response.UNAUTHORIZED

    def test_health_check(self):
        self.barrier.state.return_value = BarrierState.CLOSED
        resp = self.api.health_check()
        assert resp.status == Response.SUCCESS
        assert resp.payload["healthy"] is True


class TestOperatorAPI:
    def setup_method(self):
        self.operator_service = MagicMock()
        self.barrier = MagicMock()
        self.authorization = MagicMock()
        self.authorization.authorize.return_value = True
        self.audit = MagicMock()
        self.api = OperatorAPI(
            self.operator_service, self.barrier,
            self.authorization, self.audit
        )

    def test_authenticate_operator_success(self):
        op = make_operator()
        resp = self.api.authenticate_operator(op)
        assert resp.status == Response.SUCCESS
        assert resp.payload["authenticated"] is True

    def test_open_barrier_authorized(self):
        from communication.command_result import CommandResult
        op = make_operator()
        self.operator_service.manual_open.return_value = CommandResult.SUCCESS
        resp = self.api.open_barrier(op)
        assert resp.status == Response.SUCCESS

    def test_close_barrier_unauthorized(self):
        user = make_user(access_level=1)
        resp = self.api.close_barrier(user)
        assert resp.status == Response.UNAUTHORIZED
