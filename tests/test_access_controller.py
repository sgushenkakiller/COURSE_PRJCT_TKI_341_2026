import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from core.access_controller import AccessController
from entities.access_decision import AccessDecision
from entities.access_request import AccessRequest
from entities.direction import Direction
from entities.policy_result import PolicyResult


def make_controller(policy_result: PolicyResult = PolicyResult.ALLOW) -> tuple:
    policy = MagicMock()
    barrier = MagicMock()
    monitor = MagicMock()
    audit = MagicMock()

    decision = AccessDecision(
        request_id=str(uuid4()),
        result=policy_result,
        reason="Test decision",
    )
    policy.evaluate.return_value = decision

    from communication.command_result import CommandResult
    barrier.execute.return_value = CommandResult.SUCCESS

    controller = AccessController(
        policy=policy,
        barrier=barrier,
        monitor=monitor,
        audit=audit,
    )
    return controller, policy, barrier, monitor, audit


def make_request(uid: str = "CARD-001") -> AccessRequest:
    return AccessRequest(
        request_id=str(uuid4()),
        uid=uid,
        reader_id="reader-01",
        direction=Direction.ENTRY,
    )


def test_process_valid_request_allow():
    controller, policy, barrier, monitor, audit = make_controller(PolicyResult.ALLOW)
    request = make_request()
    decision = controller.process_request(request)
    assert decision.result == PolicyResult.ALLOW
    barrier.execute.assert_called_once()
    audit.append.assert_called()
    monitor.notify.assert_called()


def test_process_valid_request_deny():
    controller, policy, barrier, monitor, audit = make_controller(PolicyResult.DENY)
    request = make_request()
    decision = controller.process_request(request)
    assert decision.result == PolicyResult.DENY
    barrier.execute.assert_called_once()


def test_invalid_request_no_uid():
    controller, policy, barrier, monitor, audit = make_controller()
    request = AccessRequest(
        request_id=str(uuid4()),
        uid="",
        reader_id="reader-01",
        direction=Direction.ENTRY,
    )
    controller.process_request(request)
    monitor.notify.assert_called()
    audit.append.assert_called()


def test_invalid_request_no_reader():
    controller, policy, barrier, monitor, audit = make_controller()
    request = AccessRequest(
        request_id=str(uuid4()),
        uid="CARD-001",
        reader_id="",
        direction=Direction.ENTRY,
    )
    controller.process_request(request)
    monitor.notify.assert_called()
