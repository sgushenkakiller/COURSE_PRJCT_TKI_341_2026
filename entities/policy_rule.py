from dataclasses import dataclass


@dataclass(slots=True)
class PolicyRule:
    """
    Правило политики безопасности.
    """

    rule_id: str

    description: str

    enabled: bool = True

    priority: int = 0