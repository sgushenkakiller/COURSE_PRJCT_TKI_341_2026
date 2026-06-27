from abc import ABC
from abc import abstractmethod

from communication.command_result import CommandResult
from communication.commands import Command
from entities.barrier_state import BarrierState


class BarrierInterface(ABC):

    @abstractmethod
    def execute(self, command: Command) -> CommandResult:
        ...

    @abstractmethod
    def state(self) -> BarrierState:
        ...