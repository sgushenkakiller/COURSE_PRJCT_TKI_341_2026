import pytest
from uuid import uuid4

from core.access_controller import AccessController
from core.audit import AuditLogger
from core.database import AccessRepository
from core.policy_engine import PolicyEngine
from core.security_monitor import SecurityMonitor

from devices.barrier_driver import BarrierDriver

from entities.access_request import AccessRequest
from entities.administrator import Administrator
from entities.barrier_state import BarrierState
from entities.direction import Direction
from entities.operator import Operator
from entities.policy_result import PolicyResult
from entities.rfid_card import RFIDCard
from entities.user import User

from security import AuthorizationService
from services.access_service import AccessService
from services.administration_service import AdministrationService

from api.access_api import AccessAPI
from api.admin_api import AdminAPI
from api.monitor_api import MonitorAPI
from communication.responses import Response


@pytest.fixture
def system():
    repository = AccessRepository()
    monitor = SecurityMonitor()
    audit = AuditLogger(repository)
    policy = PolicyEngine(repository)
    barrier = BarrierDriver()
    controller = AccessController(policy=policy, barrier=barrier, monitor=monitor, audit=audit)
    authorization = AuthorizationService()

    access_service = AccessService(controller=controller, barrier=barrier, monitor=monitor, audit=audit)
    admin_service = AdministrationService(repository=repository, audit=audit, monitor=monitor)

    access_api = AccessAPI(access_service=access_service, authentication=None, audit=audit)
    admin_api = AdminAPI(administration_service=admin_service, authorization=authorization, audit=audit)

    from security.session import SessionService
    session_service = SessionService()
    monitor_api = MonitorAPI(
        monitor=monitor, barrier=barrier,
        session_service=session_service,
        authorization=authorization,
        audit=audit,
    )

    admin_user = Administrator(
        identifier="admin-001", full_name="Admin", access_level=3, department="IT"
    )
    repository.add_user(admin_user)

    regular_user = User(
        identifier="user-001", full_name="User One", access_level=1, department="Dev"
    )
    repository.add_user(regular_user)

    valid_card = RFIDCard(
        uid="CARD-VALID", owner_id="user-001",
        issue_date="2024-01-01", expiration_date="2026-12-31", active=True
    )
    repository.add_card(valid_card)

    return {
        "access_api": access_api,
        "admin_api": admin_api,
        "monitor_api": monitor_api,
        "repository": repository,
        "barrier": barrier,
        "monitor": monitor,
        "admin": admin_user,
    }


def test_full_access_grant_flow(system):
    resp = system["access_api"].process_card_read("CARD-VALID", "reader-01", "entry")
    assert resp.status == Response.ACCEPTED
    assert resp.payload["result"] == PolicyResult.ALLOW.value
    assert system["barrier"].state() == BarrierState.OPEN


def test_full_access_deny_unknown_card(system):
    resp = system["access_api"].process_card_read("CARD-UNKNOWN", "reader-01", "entry")
    assert resp.status == Response.REJECTED
    assert resp.payload["result"] == PolicyResult.DENY.value


def test_admin_add_and_block_user(system):
    admin = system["admin"]
    new_user = User(identifier="user-new", full_name="New", access_level=1, department="Test")
    system["admin_api"].add_user(admin, new_user)
    assert system["repository"].get_user("user-new") is not None

    system["admin_api"].block_user(admin, "user-new")
    user = system["repository"].get_user("user-new")
    assert user.blocked is True


def test_monitor_records_events_after_access(system):
    system["access_api"].process_card_read("CARD-VALID", "reader-01", "entry")
    assert system["monitor"].count() > 0


def test_audit_log_grows_after_access(system):
    initial = len(system["repository"].get_records())
    system["access_api"].process_card_read("CARD-VALID", "reader-01", "entry")
    assert len(system["repository"].get_records()) > initial


def test_admin_register_card_and_grant_access(system):
    admin = system["admin"]
    new_user = User(identifier="user-002", full_name="User Two", access_level=1, department="HR")
    system["admin_api"].add_user(admin, new_user)

    new_card = RFIDCard(
        uid="CARD-NEW", owner_id="user-002",
        issue_date="2024-01-01", expiration_date="2026-12-31", active=True
    )
    system["admin_api"].register_card(admin, new_card)

    resp = system["access_api"].process_card_read("CARD-NEW", "reader-01", "entry")
    assert resp.status == Response.ACCEPTED


def test_admin_revoke_card_denies_access(system):
    admin = system["admin"]
    system["admin_api"].revoke_card(admin, "CARD-VALID")

    resp = system["access_api"].process_card_read("CARD-VALID", "reader-01", "entry")
    assert resp.status == Response.REJECTED


def test_monitor_api_system_status(system):
    admin = system["admin"]
    resp = system["monitor_api"].get_system_status(admin)
    assert resp.status == Response.SUCCESS
    assert "barrier_state" in resp.payload
