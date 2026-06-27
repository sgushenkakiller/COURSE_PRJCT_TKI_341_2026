from dataclasses import dataclass


@dataclass(slots=True)
class Device:
    """
    Базовое устройство системы.
    """

    device_id: str

    device_type: str

    trusted: bool = False

    enabled: bool = True