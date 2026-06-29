from communication.command_result import CommandResult
from communication.commands import Command

from entities.barrier_state import BarrierState

from interfaces.barrier_interface import BarrierInterface

from .motor import BarrierMotor
from .sensor import BarrierSensor


class BarrierDriver(BarrierInterface):

    def __init__(self) -> None:

        self._motor = BarrierMotor()
        self._sensor = BarrierSensor(self._motor)

    def execute(
        self,
        command: Command
    ) -> CommandResult:

        match command:

            case Command.OPEN_BARRIER:
                self._motor.open()
                return CommandResult.SUCCESS

            case Command.CLOSE_BARRIER:
                self._motor.close()
                return CommandResult.SUCCESS

            case Command.STOP_BARRIER:
                self._motor.stop()
                return CommandResult.SUCCESS

            case Command.DENY_ACCESS:
                self._motor.close()
                return CommandResult.SUCCESS

            case _:
                return CommandResult.UNSUPPORTED

    def state(self) -> BarrierState:

        return self._sensor.state()

    def opened(self) -> bool:

        return self._sensor.is_open()

    def closed(self) -> bool:

        return self._sensor.is_closed()