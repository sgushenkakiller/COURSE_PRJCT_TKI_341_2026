import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from core.policy_engine import PolicyEngine
from core.policy_engine.decision import DecisionFactory
from entities.access_request import AccessRequest
from entities.direction import Direction
from entities.policy_result import PolicyResult
from entities.rfid_card import RFIDCard
from entities.user import User


def make_request(uid: str = "CARD-001", reader_id: str = "reader-01") -> AccessRequest:
    return AccessRequest(
        request_id=str(uuid4()),
        uid=uid,
        reader_id=reader_id,
        direction=Direction.ENTRY,
    )


def make_card(uid: str = "CARD-001", owner_id: str = "user-001", active: bool = True) -> RFIDCard:
    return RFIDCard(uid=uid, owner_id=owner_id, issue_date="2024-01-01", expiration_date="2026-12-31", active=active)


def make_user(identifier: str = "user-001", blocked: bool = False, active: bool = True, access_level: int = 1) -> User:
    return User(identifier=identifier, full_name="Test User", access_level=access_level, department="Test", blocked=blocked, active=active)


def make_policy(card: RFIDCard | None = None, user: User | None = None) -> PolicyEngine:
    repo = MagicMock()
    repo.get_card.return_value = card
    repo.get_user.return_value = user
    return PolicyEngine(repo)


def test_allow_valid_user():
    card = make_card()
    user = make_user()
    policy = make_policy(card=card, user=user)
    decision = policy.evaluate(make_request())
    assert decision.result == PolicyResult.ALLOW


def test_deny_unknown_card():
    policy = make_policy(card=None)
    decision = policy.evaluate(make_request())
    assert decision.result == PolicyResult.DENY


def test_deny_inactive_card():
    card = make_card(active=False)
    policy = make_policy(card=card)
    decision = policy.evaluate(make_request())
    assert decision.result == PolicyResult.DENY


def test_deny_blocked_user():
    card = make_card()
    user = make_user(blocked=True)
    policy = make_policy(card=card, user=user)
    decision = policy.evaluate(make_request())
    assert decision.result == PolicyResult.DENY


def test_deny_inactive_user():
    card = make_card()
    user = make_user(active=False)
    policy = make_policy(card=card, user=user)
    decision = policy.evaluate(make_request())
    assert decision.result == PolicyResult.DENY


def test_deny_zero_access_level():
    card = make_card()
    user = make_user(access_level=0)
    policy = make_policy(card=card, user=user)
    decision = policy.evaluate(make_request())
    assert decision.result == PolicyResult.DENY


def test_deny_empty_reader_id():
    card = make_card()
    user = make_user()
    policy = make_policy(card=card, user=user)
    request = make_request(reader_id="   ")
    decision = policy.evaluate(request)
    assert decision.result == PolicyResult.DENY


def test_decision_factory_allow():
    d = DecisionFactory.allow("req-1")
    assert d.result == PolicyResult.ALLOW
    assert d.request_id == "req-1"


def test_decision_factory_deny():
    d = DecisionFactory.deny("req-2", "No card")
    assert d.result == PolicyResult.DENY
    assert "No card" in d.reason
