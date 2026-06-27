from entities.barrier_state import BarrierState

from .motor import BarrierMotor


class BarrierSensor:

    def __init__(
        self,
        motor: BarrierMotor
    ) -> None:

        self._motor = motor

    def state(self) -> BarrierState:
        return self._motor.state()

    def is_open(self) -> bool:
        return self.state() == BarrierState.OPEN

    def is_closed(self) -> bool:
        return self.state() == BarrierState.CLOSED