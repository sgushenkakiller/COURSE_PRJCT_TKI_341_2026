from enum import Enum


class PolicyResult(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_OPERATOR = "require_operator"
    REQUIRE_ADMIN = "require_admin"