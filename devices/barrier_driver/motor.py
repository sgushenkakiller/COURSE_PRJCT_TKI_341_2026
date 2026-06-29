from entities.barrier_state import BarrierState


class BarrierMotor:

    def __init__(self) -> None:
        self._state = BarrierState.CLOSED

    def open(self) -> None:
        self._state = BarrierState.OPEN

    def close(self) -> None:
        self._state = BarrierState.CLOSED

    def stop(self) -> None:
        self._state = BarrierState.STOPPED

    def state(self) -> BarrierState:
        return self._state